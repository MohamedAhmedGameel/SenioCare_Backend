import express, { Router } from "express";
import dotenv from "dotenv";
import cors from "cors";
import connectDB from "./config/db.js";
import authRoutes from "./routes/auth.routes.js";
import authMiddleware from "./middleware/auth.middleware.js";
import elderRoutes from "./routes/elder.routes.js";
import caregiverRoutes from "./routes/caregiver.routes.js";
import serviceProviderRoutes from "./routes/serviceProvider.routes.js";

// swagger for api-docs
import { swaggerSpec, swaggerUiMiddleware } from "./config/swagger.js";

dotenv.config();

const app = express();
const router = express.Router();
app.use(cors());
app.use(express.json());

connectDB();


app.get('/', (req, res) => {
  res.send(`
    <title>SenioCare</title>
    <div style="display:flex; flex-direction:column; align-items:center; margin-top:50px;">
      <h1 style="font-size:50px; font-family:'Brush Script MT', cursive;">
        #1
      </h1>
      <p style="font-size:20px; font-family:'Brush Script MT', cursive;">
        For more info please read the 
        <a href="/api-docs">docs</a>
      </p>
    </div>
  `);
});


// Swagger endpoint
app.use("/api-docs", swaggerUiMiddleware.serve, swaggerUiMiddleware.setup(swaggerSpec));

app.use("/auth", authRoutes);
// Require JWT for all routes after this line
app.use(authMiddleware);
app.use("/elders", elderRoutes);
app.use("/caregivers", caregiverRoutes);
app.use("/service-providers", serviceProviderRoutes);
// app.use("/", ()=>{return"lol"});
app.listen(process.env.Port, () => console.log("Server running on port 5000"));
