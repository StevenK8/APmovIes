module.exports = {
    get: {
        tags: ["IMDB Movie"],
        description: "Get a movie rating",
        operationId: "getMovie",
        parameters: [
            {
                name: "id",
                in: "path",
                schema: {
                    $ref: "#/components/schemas/User/properties/_id"
                },
                required: true,
                description: "A single movie id",
            },
        ],
        responses: {
            200: {
                description: "Movie is obtained",
                content: {
                    "application/json": {
                        schema: {
                            $ref: "#/components/schemas/getUser"
                        }
                    }
                }
            },
            404: {
                description: "User is not found",
                content: {
                    "application/json": {
                        schema: {
                            $ref: "#/components/schemas/Error"
                        }
                    }
                }
            }
        }
    }
};