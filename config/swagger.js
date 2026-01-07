import swaggerJsdoc from "swagger-jsdoc";
import swaggerUi from "swagger-ui-express";

const swaggerDefinition = {
  openapi: "3.0.0",
  info: {
    title: "SenioCare",
    version: "1.1.0",
    description: "An AI-Powered Smart Companion for Enhancing Elderly Health, Independence, and Quality of Life",
  },
  components: {
    schemas: {
      User: {
        type: "object",
        properties: {
          _id: { type: "string", readOnly: true },
          name: { type: "string" },
          email: { type: "string" },
          avatar: { type: "string" },
          role: { type: "string" }
        },
        example: {
          _id: "67a1234567bb99aa33cc22dd",
          name: "Mohamed Gameel",
          email: "mohamed@example.com",
          avatar: "https://lh3.googleusercontent.com/...",
          role: "caregiver"
        }
      }
      ,
      Elder: {
        type: "object",
        properties: {
          _id: { type: "string", readOnly: true },
          age: { type: "number" },
          weight: { type: "number" },
          height: { type: "number" },
          gender: { type: "string" },
          chronicDiseases: { type: "array", items: { type: "string" } },
          allergies: { type: "array", items: { type: "string" } },
          caregiver_ids: { type: "array", items: { type: "string" } },
          bloodType: { type: "string" },
          mobilityStatus: { type: "string" }
        }
      },
      Caregiver: {
        type: "object",
        properties: {
          _id: { type: "string", readOnly: true },
          phone_number: { type: "string" },
          gender: { type: "string" },
          relationship: { type: "string" },
          elder_ids: { type: "array", items: { type: "string" } }
        }
      },
      ServiceProvider: {
        type: "object",
        properties: {
          _id: { type: "string", readOnly: true },
          phone_number: { type: "string" },
          specialization: { type: "string" }
        }
      }
    }
  }
  ,
  paths: {
    "/elders": {
      get: {
        summary: "List elders",
        responses: { "200": { description: "OK" } }
      },
      post: {
        summary: "Create elder",
        requestBody: { content: { "application/json": { schema: { $ref: "#/components/schemas/Elder" } } } },
        responses: { "201": { description: "Created" } }
      }
    },
    "/elders/{id}": {
      get: { summary: "Get elder", parameters: [{ name: "id", in: "path", required: true, schema: { type: "string" } }], responses: { "200": { description: "OK" } } },
      patch: { summary: "Update elder", parameters: [{ name: "id", in: "path", required: true, schema: { type: "string" } }], requestBody: { content: { "application/json": { schema: { $ref: "#/components/schemas/Elder" } } } }, responses: { "200": { description: "OK" } } },
      delete: { summary: "Delete elder", parameters: [{ name: "id", in: "path", required: true, schema: { type: "string" } }], responses: { "200": { description: "Deleted" } } }
    },
    "/caregivers": {
      get: { summary: "List caregivers", responses: { "200": { description: "OK" } } },
      post: { summary: "Create caregiver", requestBody: { content: { "application/json": { schema: { $ref: "#/components/schemas/Caregiver" } } } }, responses: { "201": { description: "Created" } } }
    },
    "/caregivers/{id}": {
      get: { summary: "Get caregiver", parameters: [{ name: "id", in: "path", required: true, schema: { type: "string" } }], responses: { "200": { description: "OK" } } },
      patch: { summary: "Update caregiver", parameters: [{ name: "id", in: "path", required: true, schema: { type: "string" } }], requestBody: { content: { "application/json": { schema: { $ref: "#/components/schemas/Caregiver" } } } }, responses: { "200": { description: "OK" } } },
      delete: { summary: "Delete caregiver", parameters: [{ name: "id", in: "path", required: true, schema: { type: "string" } }], responses: { "200": { description: "Deleted" } } }
    },
    "/service-providers": {
      get: { summary: "List service providers", responses: { "200": { description: "OK" } } },
      post: { summary: "Create service provider", requestBody: { content: { "application/json": { schema: { $ref: "#/components/schemas/ServiceProvider" } } } }, responses: { "201": { description: "Created" } } }
    },
    "/service-providers/{id}": {
      get: { summary: "Get service provider", parameters: [{ name: "id", in: "path", required: true, schema: { type: "string" } }], responses: { "200": { description: "OK" } } },
      patch: { summary: "Update service provider", parameters: [{ name: "id", in: "path", required: true, schema: { type: "string" } }], requestBody: { content: { "application/json": { schema: { $ref: "#/components/schemas/ServiceProvider" } } } }, responses: { "200": { description: "OK" } } },
      delete: { summary: "Delete service provider", parameters: [{ name: "id", in: "path", required: true, schema: { type: "string" } }], responses: { "200": { description: "Deleted" } } }
    }
  }
};

const options = {
  definition: swaggerDefinition,
  apis: ["./routes/*.js"], // Path to your route docs
};

export const swaggerSpec = swaggerJsdoc(options);
export const swaggerUiMiddleware = swaggerUi;
