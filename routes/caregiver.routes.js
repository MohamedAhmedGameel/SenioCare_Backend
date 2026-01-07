import express from "express";
import {
  createCaregiver,
  listCaregivers,
  getCaregiver,
  updateCaregiver,
  deleteCaregiver,
} from "../controllers/caregiver.controller.js";

const router = express.Router();

/**
 * @swagger
 * tags:
 *   name: Caregivers
 *   description: Caregiver records management
 */

/**
 * @swagger
 * /caregivers:
 *   get:
 *     summary: List caregivers
 *     tags: [Caregivers]
 *     responses:
 *       200:
 *         description: Array of caregivers
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Caregiver'
 *       500:
 *         description: Server error
 *   post:
 *     summary: Create a new caregiver
 *     tags: [Caregivers]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/Caregiver'
 *     responses:
 *       201:
 *         description: Caregiver created
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Caregiver'
 *       500:
 *         description: Server error
 */

/**
 * @swagger
 * /caregivers/{id}:
 *   get:
 *     summary: Get a caregiver by id
 *     tags: [Caregivers]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Caregiver object
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Caregiver'
 *       404:
 *         description: Not found
 *   patch:
 *     summary: Update a caregiver (partial update)
 *     tags: [Caregivers]
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
 *             $ref: '#/components/schemas/Caregiver'
 *     responses:
 *       200:
 *         description: Updated caregiver
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Caregiver'
 *       404:
 *         description: Not found
 *   delete:
 *     summary: Delete a caregiver
 *     tags: [Caregivers]
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

router.get("/", listCaregivers);
router.get("/:id", getCaregiver);
router.post("/", createCaregiver);
router.patch("/:id", updateCaregiver);
router.delete("/:id", deleteCaregiver);

export default router;
