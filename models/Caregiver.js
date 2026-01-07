import mongoose from "mongoose";

const caregiverSchema = new mongoose.Schema({
  phone_number: String,
  gender: String,
  relationship: { type: String, enum: ["son", "daughter", "nurse", "other"], default: "other" },
  elder_ids: [{ type: mongoose.Schema.Types.ObjectId, ref: "Elder" }],
}, { timestamps: true });

export default mongoose.model("Caregiver", caregiverSchema);
