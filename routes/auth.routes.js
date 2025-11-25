import express from "express";
import { googleAuth } from "../controllers/auth.controller.js";

const router = express.Router();

// POST /auth/google
router.post("/google", googleAuth);

export default router;
