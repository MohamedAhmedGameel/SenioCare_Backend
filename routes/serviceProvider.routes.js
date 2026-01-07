import express from "express";
import {
  createServiceProvider,
  listServiceProviders,
  getServiceProvider,
  updateServiceProvider,
  deleteServiceProvider,
} from "../controllers/serviceProvider.controller.js";

const router = express.Router();

/**
 * @swagger
 * tags:
 *   name: ServiceProviders
 *   description: Service provider records management
 */

/**
 * @swagger
 * /service-providers:
 *   get:
 *     summary: List service providers
 *     tags: [ServiceProviders]
 *     responses:
 *       200:
 *         description: Array of service providers
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/ServiceProvider'
 *       500:
 *         description: Server error
 *   post:
 *     summary: Create a new service provider
 *     tags: [ServiceProviders]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/ServiceProvider'
 *     responses:
 *       201:
 *         description: Service provider created
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ServiceProvider'
 *       500:
 *         description: Server error
 */

/**
 * @swagger
 * /service-providers/{id}:
 *   get:
 *     summary: Get a service provider by id
 *     tags: [ServiceProviders]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Service provider object
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ServiceProvider'
 *       404:
 *         description: Not found
 *   patch:
 *     summary: Update a service provider (partial update)
 *     tags: [ServiceProviders]
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
 *             $ref: '#/components/schemas/ServiceProvider'
 *     responses:
 *       200:
 *         description: Updated service provider
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/ServiceProvider'
 *       404:
 *         description: Not found
 *   delete:
 *     summary: Delete a service provider
 *     tags: [ServiceProviders]
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

router.get("/", listServiceProviders);
router.get("/:id", getServiceProvider);
router.post("/", createServiceProvider);
router.patch("/:id", updateServiceProvider);
router.delete("/:id", deleteServiceProvider);

export default router;
