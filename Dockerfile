FROM golang:alpine as build

RUN apk add gcc sqlite-dev build-base

WORKDIR /streambot

COPY go.mod go.sum ./
RUN go mod download

COPY . .

# Deployment needs alpine for a CA, so we allow CGO
RUN go build

# Using alpine instead of scratch so that we have an up-to-date certificate authority
FROM alpine:latest

COPY --from=build /streambot/streambot .

ENTRYPOINT ["./streambot"]
