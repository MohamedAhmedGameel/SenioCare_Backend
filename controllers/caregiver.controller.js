import mongoose from "mongoose";
import Caregiver from "../models/Caregiver.js";

const pickProvided = (body) => {
  const doc = {};
  Object.keys(body).forEach((k) => {
    if (k === "_id" || k === "id") return;
    if (body[k] !== undefined) doc[k] = body[k];
  });
  return doc;
};

export const createCaregiver = async (req, res) => {
  try {
    const doc = pickProvided(req.body);
    const cg = await Caregiver.create(doc);
    res.status(201).json(cg);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const listCaregivers = async (req, res) => {
  try {
    const list = await Caregiver.find().populate("elder_ids");
    res.json(list);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const getCaregiver = async (req, res) => {
  try {
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) return res.status(400).json({ message: "Invalid id" });
    const cg = await Caregiver.findById(req.params.id).populate("elder_ids");
    if (!cg) return res.status(404).json({ message: "Not found" });
    res.json(cg);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const updateCaregiver = async (req, res) => {
  try {
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) return res.status(400).json({ message: "Invalid id" });
    const cg = await Caregiver.findById(req.params.id);
    if (!cg) return res.status(404).json({ message: "Not found" });
    const updates = pickProvided(req.body);
    Object.keys(updates).forEach((k) => (cg[k] = updates[k]));
    await cg.save();
    res.json(cg);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const deleteCaregiver = async (req, res) => {
  try {
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) return res.status(400).json({ message: "Invalid id" });
    const cg = await Caregiver.findByIdAndDelete(req.params.id);
    if (!cg) return res.status(404).json({ message: "Not found" });
    res.json({ message: "Deleted" });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
