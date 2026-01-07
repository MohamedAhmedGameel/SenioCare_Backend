import mongoose from "mongoose";

const serviceProviderSchema = new mongoose.Schema({
  phone_number: String,
  specialization: String,
}, { timestamps: true });

export default mongoose.model("ServiceProvider", serviceProviderSchema);
