"""API local de contingência para a Plataforma de Estudos.

Usa apenas a biblioteca padrão do Python e SQLite, para que o projeto possa
ser demonstrado sem depender de serviços externos. Não substitui a futura API
Spring Boot: é uma implementação isolada nesta branch de contingência.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import sqlite3
import sys
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[1]
UI_DIR = ROOT / "UI"
DB_PATH = Path(os.getenv("PLATAFORMA_DB_PATH", ROOT / "backend" / "data" / "plataforma.db"))
HOST = os.getenv("PLATAFORMA_HOST", "127.0.0.1")
PORT = int(os.getenv("PLATAFORMA_PORT", "8080"))

if str(UI_DIR) not in sys.path:
    sys.path.insert(0, str(UI_DIR))
from mock_data import EXERCICIOS  # noqa: E402

QUESTIONS = [question for questions in EXERCICIOS.values() for question in questions]
QUESTION_BY_ID = {int(question["id"]): question for question in QUESTIONS}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('STUDENT', 'GUARDIAN')),
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                question_id INTEGER NOT NULL,
                option_id INTEGER NOT NULL,
                correct INTEGER NOT NULL,
                points_awarded INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS guardian_students (
                guardian_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                student_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                created_at TEXT NOT NULL,
                PRIMARY KEY (guardian_id, student_id)
            );
            """
        )


def hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 390_000)
    return f"{salt.hex()}${digest.hex()}"


def password_matches(password: str, stored: str) -> bool:
    try:
        salt_hex, digest_hex = stored.split("$", 1)
        candidate = hash_password(password, bytes.fromhex(salt_hex)).split("$", 1)[1]
        return secrets.compare_digest(candidate, digest_hex)
    except ValueError:
        return False


def public_user(row: sqlite3.Row) -> dict:
    return {"id": row["id"], "name": row["name"], "email": row["email"], "role": row["role"]}


def public_question(question: dict) -> dict:
    return {
        key: value
        for key, value in question.items()
        if key not in {"correta", "explicacao"}
    } | {
        "alternativas": [
            {key: value for key, value in option.items() if key != "correta"}
            for option in question["alternativas"]
        ]
    }


def progress_for_student(conn: sqlite3.Connection, student_id: int) -> dict:
    rows = conn.execute(
        "SELECT question_id, correct, points_awarded FROM attempts WHERE user_id = ?", (student_id,)
    ).fetchall()
    answered = {int(row["question_id"]) for row in rows}
    correct = {int(row["question_id"]) for row in rows if row["correct"]}
    score = sum(int(row["points_awarded"]) for row in rows)
    by_subject = {}
    for subject in ("MATEMATICA", "GEOGRAFIA"):
        ids = {question_id for question_id in answered if QUESTION_BY_ID.get(question_id, {}).get("materia") == subject}
        correct_ids = ids & correct
        by_subject[subject] = {
            "respondidas": len(ids),
            "acertos": len(correct_ids),
            "erros": len(ids - correct_ids),
            "total_questoes": sum(1 for question in QUESTIONS if question.get("materia") == subject),
        }
    return {
        "respondidas": len(answered),
        "acertos": len(correct),
        "erros": len(answered - correct),
        "pontuacao": score,
        "por_materia": by_subject,
    }


class ApiHandler(BaseHTTPRequestHandler):
    server_version = "PlataformaEstudos/1.0"

    def log_message(self, format: str, *args) -> None:
        print(f"[{now()}] {self.address_string()} - {format % args}")

    def send_json(self, status: int, payload: dict | list) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > 100_000:
            raise ValueError("Corpo da requisição inválido.")
        try:
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("JSON inválido.") from exc
        if not isinstance(data, dict):
            raise ValueError("JSON deve ser um objeto.")
        return data

    def current_user(self, conn: sqlite3.Connection) -> sqlite3.Row:
        value = self.headers.get("Authorization", "")
        if not value.startswith("Bearer "):
            raise PermissionError("Faça login para continuar.")
        token = value.removeprefix("Bearer ").strip()
        row = conn.execute(
            "SELECT u.* FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token = ?", (token,)
        ).fetchone()
        if row is None:
            raise PermissionError("Sessão inválida. Faça login novamente.")
        return row

    def require_role(self, user: sqlite3.Row, role: str) -> None:
        if user["role"] != role:
            raise PermissionError("Esta ação não está disponível para este tipo de usuário.")

    def do_OPTIONS(self) -> None:
        self.send_json(HTTPStatus.NO_CONTENT, {})

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        try:
            with connection() as conn:
                if parsed.path == "/api/health":
                    self.send_json(HTTPStatus.OK, {"status": "ok", "questoes": len(QUESTIONS)})
                    return
                if parsed.path == "/api/questions":
                    self.current_user(conn)
                    subject = parse_qs(parsed.query).get("materia", [""])[0].upper()
                    questions = QUESTIONS if not subject else [q for q in QUESTIONS if q.get("materia") == subject]
                    self.send_json(HTTPStatus.OK, [public_question(question) for question in questions])
                    return
                if parsed.path == "/api/me/progress":
                    user = self.current_user(conn)
                    self.require_role(user, "STUDENT")
                    self.send_json(HTTPStatus.OK, progress_for_student(conn, int(user["id"])))
                    return
                if parsed.path == "/api/guardian/students":
                    user = self.current_user(conn)
                    self.require_role(user, "GUARDIAN")
                    students = conn.execute(
                        """SELECT u.* FROM guardian_students gs
                           JOIN users u ON u.id = gs.student_id
                           WHERE gs.guardian_id = ? ORDER BY u.name""",
                        (user["id"],),
                    ).fetchall()
                    self.send_json(
                        HTTPStatus.OK,
                        [{"aluno": public_user(student), "progresso": progress_for_student(conn, int(student["id"]))} for student in students],
                    )
                    return
            self.send_json(HTTPStatus.NOT_FOUND, {"erro": "Rota não encontrada."})
        except PermissionError as exc:
            self.send_json(HTTPStatus.UNAUTHORIZED, {"erro": str(exc)})
        except Exception as exc:  # pragma: no cover - proteção da API em demonstração
            self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"erro": f"Erro interno: {exc}"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        try:
            data = self.read_json()
            with connection() as conn:
                if parsed.path == "/api/auth/register":
                    name = str(data.get("name", "")).strip()
                    email = str(data.get("email", "")).strip().lower()
                    password = str(data.get("password", ""))
                    role = str(data.get("role", "")).upper()
                    role = {"ALUNO": "STUDENT", "RESPONSAVEL": "GUARDIAN"}.get(role, role)
                    if len(name) < 2 or "@" not in email or len(password) < 6 or role not in {"STUDENT", "GUARDIAN"}:
                        raise ValueError("Informe nome, e-mail válido, senha de ao menos 6 caracteres e perfil.")
                    try:
                        cursor = conn.execute(
                            "INSERT INTO users(name, email, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?)",
                            (name, email, hash_password(password), role, now()),
                        )
                    except sqlite3.IntegrityError as exc:
                        raise ValueError("Já existe uma conta com este e-mail.") from exc
                    user = conn.execute("SELECT * FROM users WHERE id = ?", (cursor.lastrowid,)).fetchone()
                    token = secrets.token_urlsafe(32)
                    conn.execute("INSERT INTO sessions(token, user_id, created_at) VALUES (?, ?, ?)", (token, user["id"], now()))
                    self.send_json(HTTPStatus.CREATED, {"token": token, "user": public_user(user)})
                    return
                if parsed.path == "/api/auth/login":
                    email = str(data.get("email", "")).strip().lower()
                    password = str(data.get("password", ""))
                    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
                    if user is None or not password_matches(password, user["password_hash"]):
                        raise PermissionError("E-mail ou senha inválidos.")
                    token = secrets.token_urlsafe(32)
                    conn.execute("INSERT INTO sessions(token, user_id, created_at) VALUES (?, ?, ?)", (token, user["id"], now()))
                    self.send_json(HTTPStatus.OK, {"token": token, "user": public_user(user)})
                    return
                if parsed.path == "/api/attempts":
                    user = self.current_user(conn)
                    self.require_role(user, "STUDENT")
                    question_id, option_id = int(data.get("question_id")), int(data.get("option_id"))
                    question = QUESTION_BY_ID.get(question_id)
                    if question is None:
                        raise ValueError("Questão não encontrada.")
                    option = next((item for item in question["alternativas"] if int(item["id"]) == option_id), None)
                    if option is None:
                        raise ValueError("Alternativa não pertence a esta questão.")
                    correct = bool(option["correta"])
                    previous = conn.execute(
                        "SELECT 1 FROM attempts WHERE user_id = ? AND question_id = ? AND correct = 1 LIMIT 1",
                        (user["id"], question_id),
                    ).fetchone()
                    points = 10 if correct and previous is None else 0
                    conn.execute(
                        """INSERT INTO attempts(user_id, question_id, option_id, correct, points_awarded, created_at)
                           VALUES (?, ?, ?, ?, ?, ?)""",
                        (user["id"], question_id, option_id, int(correct), points, now()),
                    )
                    self.send_json(
                        HTTPStatus.OK,
                        {"correta": correct, "pontos_ganhos": points, "explicacao": question.get("explicacao", ""), "progresso": progress_for_student(conn, int(user["id"]))},
                    )
                    return
                if parsed.path == "/api/guardian/link":
                    guardian = self.current_user(conn)
                    self.require_role(guardian, "GUARDIAN")
                    email = str(data.get("student_email", "")).strip().lower()
                    student = conn.execute("SELECT * FROM users WHERE email = ? AND role = 'STUDENT'", (email,)).fetchone()
                    if student is None:
                        raise ValueError("Aluno não encontrado. Ele precisa criar a conta primeiro.")
                    conn.execute(
                        "INSERT OR IGNORE INTO guardian_students(guardian_id, student_id, created_at) VALUES (?, ?, ?)",
                        (guardian["id"], student["id"], now()),
                    )
                    self.send_json(HTTPStatus.OK, {"mensagem": "Aluno vinculado com sucesso."})
                    return
            self.send_json(HTTPStatus.NOT_FOUND, {"erro": "Rota não encontrada."})
        except PermissionError as exc:
            self.send_json(HTTPStatus.UNAUTHORIZED, {"erro": str(exc)})
        except (TypeError, ValueError) as exc:
            self.send_json(HTTPStatus.BAD_REQUEST, {"erro": str(exc)})
        except Exception as exc:  # pragma: no cover - proteção da API em demonstração
            self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"erro": f"Erro interno: {exc}"})


def main() -> None:
    init_db()
    print(f"API disponível em http://{HOST}:{PORT}/api/health")
    ThreadingHTTPServer((HOST, PORT), ApiHandler).serve_forever()


if __name__ == "__main__":
    main()
