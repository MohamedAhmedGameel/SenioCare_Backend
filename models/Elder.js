import mongoose from "mongoose";

const elderSchema = new mongoose.Schema({
  age: Number,
  weight: Number,
  height: Number,
  gender: String,
  chronicDiseases: [String],
  allergies: [String],
  caregiver_ids: [{ type: mongoose.Schema.Types.ObjectId, ref: "Caregiver" }],
  bloodType: String,
  mobilityStatus: String,
}, { timestamps: true });

export default mongoose.model("Elder", elderSchema);
