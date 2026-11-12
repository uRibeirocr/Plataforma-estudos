# API Java (Spring Boot). Contexto de build = raiz do repositório:
#   docker build -t plataforma-api .
#   docker run -p 8080:8080 -e DATABASE_URL=... -e DATABASE_USER=... -e DATABASE_PASSWORD=... -e JWT_SECRET=... plataforma-api
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /src
COPY backend/pom.xml backend/pom.xml
COPY conteudo conteudo
COPY backend/src backend/src
RUN mvn -B -ntp -f backend/pom.xml -DskipTests package

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /src/backend/target/educa-visual-api.jar app.jar
COPY frontend/assets /app/imagens
ENV SPRING_PROFILES_ACTIVE=prod \
    IMAGENS_DIR=/app/imagens
EXPOSE 8080
USER 1000
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
