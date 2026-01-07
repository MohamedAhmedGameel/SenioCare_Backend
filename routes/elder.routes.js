import express from "express";
import {
  createElder,
  listElders,
  getElder,
  updateElder,
  deleteElder,
} from "../controllers/elder.controller.js";

const router = express.Router();

/**
 * @swagger
 * tags:
 *   name: Elders
 *   description: Elder records management
 */

/**
 * @swagger
 * /elders:
 *   get:
 *     summary: List elders
 *     tags: [Elders]
 *     responses:
 *       200:
 *         description: Array of elders
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Elder'
 *       500:
 *         description: Server error
 *   post:
 *     summary: Create a new elder (only provided fields applied)
 *     tags: [Elders]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/Elder'
 *     responses:
 *       201:
 *         description: Elder created
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Elder'
 *       500:
 *         description: Server error
 */

/**
 * @swagger
 * /elders/{id}:
 *   get:
 *     summary: Get an elder by id
 *     tags: [Elders]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Elder object
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Elder'
 *       404:
 *         description: Not found
 *   patch:
 *     summary: Update an elder (partial update)
 *     tags: [Elders]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     requestBody:
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/Elder'
 *     responses:
 *       200:
 *         description: Updated elder
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Elder'
 *       404:
 *         description: Not found
 *   delete:
 *     summary: Delete an elder
 *     tags: [Elders]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Deleted
 *       404:
 *         description: Not found
 */

router.get("/", listElders);
router.get("/:id", getElder);
router.post("/", createElder);
router.patch("/:id", updateElder);
router.delete("/:id", deleteElder);

export default router;
