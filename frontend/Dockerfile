FROM node:16-alpine3.11 as build
# FROM mhart/alpine-node:slim-12

# install dependencies
WORKDIR /app
COPY . .
# COPY package.json package-lock.json ./
RUN apk add --update npm
RUN npm i

# Copy all local files into the image.

RUN npm run build

# ###
# # Only copy over the Node pieces we need
# # ~> Saves 35MB
# ###
# \FROM node:16-alpine-node3.11

# WORKDIR /app
# COPY --from=build /app .
# COPY . .

EXPOSE 3000
CMD ["node", "build"]
