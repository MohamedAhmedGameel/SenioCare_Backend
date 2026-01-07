import mongoose from "mongoose";
import ServiceProvider from "../models/ServiceProvider.js";

const pickProvided = (body) => {
  const doc = {};
  Object.keys(body).forEach((k) => {
    if (k === "_id" || k === "id") return;
    if (body[k] !== undefined) doc[k] = body[k];
  });
  return doc;
};

export const createServiceProvider = async (req, res) => {
  try {
    const doc = pickProvided(req.body);
    const sp = await ServiceProvider.create(doc);
    res.status(201).json(sp);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const listServiceProviders = async (req, res) => {
  try {
    const list = await ServiceProvider.find();
    res.json(list);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const getServiceProvider = async (req, res) => {
  try {
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) return res.status(400).json({ message: "Invalid id" });
    const sp = await ServiceProvider.findById(req.params.id);
    if (!sp) return res.status(404).json({ message: "Not found" });
    res.json(sp);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const updateServiceProvider = async (req, res) => {
  try {
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) return res.status(400).json({ message: "Invalid id" });
    const sp = await ServiceProvider.findById(req.params.id);
    if (!sp) return res.status(404).json({ message: "Not found" });
    const updates = pickProvided(req.body);
    Object.keys(updates).forEach((k) => (sp[k] = updates[k]));
    await sp.save();
    res.json(sp);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

export const deleteServiceProvider = async (req, res) => {
  try {
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) return res.status(400).json({ message: "Invalid id" });
    const sp = await ServiceProvider.findByIdAndDelete(req.params.id);
    if (!sp) return res.status(404).json({ message: "Not found" });
    res.json({ message: "Deleted" });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
