import swaggerJsdoc from "swagger-jsdoc";
import swaggerUi from "swagger-ui-express";

const options = {
  definition: {
    openapi: "3.0.0",
    info: {
      title: "SenioCare",
      version: "1.0.0",
      description: "An AI-Powered Smart Companion for Enhancing Elderly Health, Independence, and Quality of Life",
    },
    servers: [
      {
        url: "https://senio-care-backend.vercel.app",
      },
    ],
  },
  apis: ["./routes/*.js"], // IMPORTANT: Where Swagger should read JSDoc comments
};

const swaggerDefinition = {
  openapi: "3.0.0",
  info: {
    title: "SenioCare",
    version: "1.0.0",
    description: "An AI-Powered Smart Companion for Enhancing Elderly Health, Independence, and Quality of Life",
  },
  components: {
    schemas: {
      User: {
        type: "object",
        properties: {
          _id: { type: "string" },
          name: { type: "string" },
          email: { type: "string" },
          avatar: { type: "string" },
          provider: { type: "string" },
          providerId: { type: "string" }
        },
        example: {
          _id: "67a1234567bb99aa33cc22dd",
          name: "Mohamed Gameel",
          email: "mohamed@example.com",
          avatar: "https://lh3.googleusercontent.com/...",
          provider: "google",
          providerId: "11223344556677889900"
        }
      }
    }
  },
};

export const swaggerSpec = swaggerJsdoc(options);
export const swaggerUiMiddleware = swaggerUi;
