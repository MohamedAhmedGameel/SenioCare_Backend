import express from "express";
import { googleAuth } from "../controllers/auth.controller.js";

const router = express.Router();

/**
 * @swagger
 * tags:
 *   name: Authentication
 *   description: Google OAuth (idToken) based login/register
 */

/**
 * @swagger
 * /auth/google:
 *   post:
 *     summary: Authenticate user using Google idToken (from Flutter)
 *     tags: [Authentication]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               idToken:
 *                 type: string
 *                 description: Google ID Token from Flutter Google Sign-In
 *                 example: eyJhbGciOiJSUzI1NiIsImtpZCI6Ij...
 *               role:
 *                 type: string
 *                 example: caregiver
 *     responses:
 *       200:
 *         description: User authenticated
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 message:
 *                   type: string
 *                   example: Authenticated
 *                 token:
 *                   type: string
 *                   example: eyJhbGciOiJIUzI1...
 *                 user:
 *                   $ref: '#/components/schemas/User'
 *       400:
 *         description: Missing or invalid token
 *       500:
 *         description: Server error
 */

router.post("/google", googleAuth);

export default router;
