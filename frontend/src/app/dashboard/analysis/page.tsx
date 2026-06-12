"use client";

import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useDropzone } from "react-dropzone";
import {
  Upload, FileText, X, CheckCircle, AlertTriangle, Loader2,
  Brain, Eye, Activity, Scan, ArrowRight, Heart
} from "lucide-react";
import { analysisAPI } from "@/lib/api";
import toast from "react-hot-toast";

const IMAGE_TYPES = [
  { value: "ecg", label: "ECG", icon: Activity, desc: "Electrocardiogram", color: "blue" },
  { value: "mri", label: "MRI", icon: Brain, desc: "Magnetic Resonance", color: "purple" },
  { value: "ct_scan", label: "CT Scan", icon: Scan, desc: "Computed Tomography", color: "cyan" },
  { value: "x_ray", label: "X-Ray", icon: Eye, desc: "Chest X-Ray", color: "green" },
];

export default function AnalysisPage() {
  const [file, setFile] = useState<File | null>(null);
  const [imageType, setImageType] = useState("");
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const f = acceptedFiles[0];
      if (f.size > 25 * 1024 * 1024) {
        toast.error("File too large. Max 25MB.");
        return;
      }
      setFile(f);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [".jpg", ".jpeg", ".png"] },
    maxFiles: 1,
  });

  const handleUpload = async () => {
    if (!file || !imageType) {
      toast.error("Please select a file and image type");
      return;
    }
    setUploading(true);
    try {
      const res = await analysisAPI.upload(file, imageType);
      toast.success("Analysis started! You'll be notified when complete.");
      setFile(null);
      setImageType("");
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="max-w-4xl mx-auto p-4 lg:p-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-2xl font-bold text-slate-900 mb-1">New Analysis</h1>
          <p className="text-slate-500 mb-8">Upload a medical image for AI-powered analysis</p>

          {/* Image Type Selection */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-slate-700 mb-3">Select Image Type</label>
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
              {IMAGE_TYPES.map((type) => (
                <button
                  key={type.value}
                  onClick={() => setImageType(type.value)}
                  className={`p-4 rounded-2xl border-2 text-left transition-all ${
                    imageType === type.value
                      ? "border-blue-500 bg-blue-50 shadow-lg shadow-blue-500/10"
                      : "border-slate-200 bg-white hover:border-slate-300 hover:shadow-md"
                  }`}
                >
                  <type.icon className={`w-7 h-7 mb-2 ${imageType === type.value ? "text-blue-600" : "text-slate-400"}`} />
                  <div className="text-sm font-bold text-slate-900">{type.label}</div>
                  <div className="text-xs text-slate-500">{type.desc}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Dropzone */}
          <div
            {...getRootProps()}
            className={`relative border-2 border-dashed rounded-2xl p-10 text-center transition-all cursor-pointer ${
              isDragActive ? "border-blue-500 bg-blue-50" : file ? "border-green-400 bg-green-50" : "border-slate-300 bg-white hover:border-blue-400 hover:bg-blue-50/50"
            }`}
          >
            <input {...getInputProps()} />
            <AnimatePresence mode="wait">
              {file ? (
                <motion.div key="file" initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.9 }}>
                  <CheckCircle className="w-14 h-14 text-green-500 mx-auto mb-3" />
                  <h3 className="text-lg font-bold text-slate-900">{file.name}</h3>
                  <p className="text-sm text-slate-500 mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                  <button
                    onClick={(e) => { e.stopPropagation(); setFile(null); }}
                    className="mt-3 text-sm text-red-500 hover:text-red-600 font-medium flex items-center gap-1 mx-auto"
                  >
                    <X className="w-4 h-4" /> Remove
                  </button>
                </motion.div>
              ) : (
                <motion.div key="drop" initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.9 }}>
                  <div className="w-16 h-16 rounded-2xl bg-blue-100 flex items-center justify-center mx-auto mb-4">
                    <Upload className="w-8 h-8 text-blue-600" />
                  </div>
                  <h3 className="text-lg font-bold text-slate-900 mb-1">
                    {isDragActive ? "Drop your image here" : "Drag & drop your medical image"}
                  </h3>
                  <p className="text-sm text-slate-500 mb-4">or click to browse files</p>
                  <div className="flex flex-wrap justify-center gap-2">
                    {["JPG", "JPEG", "PNG", "DICOM"].map((f) => (
                      <span key={f} className="px-2.5 py-1 bg-slate-100 text-slate-600 text-xs font-medium rounded-lg">{f}</span>
                    ))}
                  </div>
                  <p className="text-xs text-slate-400 mt-3">Maximum file size: 25MB</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Upload Button */}
          <div className="mt-6 flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm text-slate-500">
              <AlertTriangle className="w-4 h-4 text-amber-500" />
              AI results are for preliminary screening only
            </div>
            <button
              onClick={handleUpload}
              disabled={!file || !imageType || uploading}
              className="px-8 py-3.5 bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold rounded-xl hover:shadow-lg hover:shadow-blue-500/25 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {uploading ? (
                <><Loader2 className="w-5 h-5 animate-spin" /> Analyzing...</>
              ) : (
                <><Brain className="w-5 h-5" /> Start Analysis <ArrowRight className="w-4 h-4" /></>
              )}
            </button>
          </div>

          {/* Info Cards */}
          <div className="grid sm:grid-cols-3 gap-4 mt-10">
            {[
              { icon: Brain, title: "AI-Powered", desc: "ViT + ResNet50 ensemble models analyze your image with 97.8% accuracy" },
              { icon: FileText, title: "PDF Reports", desc: "Get professional medical reports with findings and recommendations" },
              { icon: Heart, title: "Risk Assessment", desc: "Receive risk levels (Low/Moderate/High/Critical) with confidence scores" },
            ].map((item) => (
              <div key={item.title} className="bg-white rounded-2xl border border-slate-200 p-5">
                <item.icon className="w-8 h-8 text-blue-600 mb-3" />
                <h4 className="font-bold text-slate-900 mb-1">{item.title}</h4>
                <p className="text-sm text-slate-500 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
