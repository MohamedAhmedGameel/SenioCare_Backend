import mongoose from "mongoose";
import Elder from "../models/Elder.js";

const pickProvided = (body) => {
  const doc = {};
  Object.keys(body).forEach((k) => {
    if (k === "_id" || k === "id") return;
    if (body[k] !== undefined) doc[k] = body[k];
  });
  return doc;
};

export const createElder = async (req, res) => {
  try {
    const doc = pickProvided(req.body);
    const elder = await Elder.create(doc);
    res.status(201).json(elder);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const listElders = async (req, res) => {
  try {
    const elders = await Elder.find().populate("caregiver_ids");
    res.json(elders);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const getElder = async (req, res) => {
  try {
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) return res.status(400).json({ message: "Invalid id" });
    const elder = await Elder.findById(req.params.id).populate("caregiver_ids");
    if (!elder) return res.status(404).json({ message: "Not found" });
    res.json(elder);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const updateElder = async (req, res) => {
  try {
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) return res.status(400).json({ message: "Invalid id" });
    const elder = await Elder.findById(req.params.id);
    if (!elder) return res.status(404).json({ message: "Not found" });

    const updates = pickProvided(req.body);
    Object.keys(updates).forEach((k) => (elder[k] = updates[k]));

    await elder.save();
    res.json(elder);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const deleteElder = async (req, res) => {
  try {
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) return res.status(400).json({ message: "Invalid id" });
    const elder = await Elder.findByIdAndDelete(req.params.id);
    if (!elder) return res.status(404).json({ message: "Not found" });
    res.json({ message: "Deleted" });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
