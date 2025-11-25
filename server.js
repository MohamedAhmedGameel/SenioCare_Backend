import express, { Router } from "express";
import dotenv from "dotenv";
import cors from "cors";
import connectDB from "./config/db.js";
import authRoutes from "./routes/auth.routes.js";

dotenv.config();

const app = express();
const router = express.Router();
app.use(cors());
app.use(express.json());

connectDB();


app.get('/', (req, res) => {
  res.send('لسه يا نجم')
})

app.use("/auth", authRoutes);
// app.use("/", ()=>{return"lol"});
app.listen(process.env.Port, () => console.log("Server running on port 5000"));
