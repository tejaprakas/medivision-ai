"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import {
  Heart, Upload, FileText, MessageSquare, Calendar, Bell,
  Activity, TrendingUp, Clock, ChevronRight, AlertTriangle,
  CheckCircle,Brain, Eye, BarChart3, Settings, LogOut, Menu, X
} from "lucide-react";
import { useAuthStore } from "@/store/authStore";
import { analysisAPI, notificationsAPI, reportsAPI } from "@/lib/api";
import type { AnalysisResult, Notification, MedicalReport } from "@/types";

export default function PatientDashboard() {
  const { user, logout } = useAuthStore();
  const [analyses, setAnalyses] = useState<AnalysisResult[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [reports, setReports] = useState<MedicalReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [aRes, nRes, rRes] = await Promise.all([
          analysisAPI.getResults(0, 5),
          notificationsAPI.getAll(true),
          reportsAPI.getMyReports(),
        ]);
        setAnalyses(aRes.data);
        setNotifications(nRes.data);
        setReports(rRes.data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const healthScore = 85;
  const riskColor = (level: string) => {
    if (level === "low") return "#10B981";
    if (level === "moderate") return "#F59E0B";
    if (level === "high") return "#EF4444";
    return "#7C3AED";
  };

  const navItems = [
    { icon: BarChart3, label: "Dashboard", href: "/dashboard/patient", active: true },
    { icon: Upload, label: "New Analysis", href: "/dashboard/analysis" },
    { icon: MessageSquare, label: "AI Chatbot", href: "/dashboard/chatbot" },
    { icon: FileText, label: "Reports", href: "/dashboard/reports" },
    { icon: Calendar, label: "Appointments", href: "/dashboard/patient#appointments" },
    { icon: Settings, label: "Settings", href: "/dashboard/patient#settings" },
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar */}
      <aside className={`fixed lg:static inset-y-0 left-0 z-50 w-64 bg-white border-r border-slate-200 transform transition-transform ${sidebarOpen ? "translate-x-0" : "-translate-x-full"} lg:translate-x-0`}>
        <div className="p-5 border-b border-slate-100">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-600 to-cyan-500 flex items-center justify-center">
              <Heart className="w-5 h-5 text-white" fill="white" />
            </div>
            <span className="text-lg font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">MediVision AI</span>
          </Link>
        </div>
        <nav className="p-3 space-y-1">
          {navItems.map((item) => (
            <Link key={item.label} href={item.href}
              className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${item.active ? "bg-blue-50 text-blue-700" : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"}`}>
              <item.icon className="w-5 h-5" />
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="absolute bottom-0 left-0 right-0 p-3 border-t border-slate-100">
          <button onClick={() => { logout(); window.location.href = "/"; }}
            className="flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium text-slate-600 hover:bg-red-50 hover:text-red-600 w-full transition-all">
            <LogOut className="w-5 h-5" /> Sign Out
          </button>
        </div>
      </aside>

      {/* Overlay */}
      {sidebarOpen && <div className="fixed inset-0 bg-black/30 z-40 lg:hidden" onClick={() => setSidebarOpen(false)} />}

      {/* Main Content */}
      <main className="flex-1 min-w-0">
        {/* Top Bar */}
        <header className="sticky top-0 z-30 bg-white/80 backdrop-blur-xl border-b border-slate-200 px-4 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button onClick={() => setSidebarOpen(true)} className="lg:hidden p-2 rounded-lg hover:bg-slate-100">
              <Menu className="w-5 h-5" />
            </button>
            <h1 className="text-lg font-bold text-slate-900">Patient Dashboard</h1>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/dashboard/chatbot" className="relative p-2 rounded-xl hover:bg-slate-100 transition-colors">
              <Bell className="w-5 h-5 text-slate-500" />
              {notifications.length > 0 && <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-white" />}
            </Link>
            <div className="flex items-center gap-2.5 pl-3 border-l border-slate-200">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-white font-bold text-sm">
                {user?.full_name?.charAt(0) || "U"}
              </div>
              <div className="hidden sm:block">
                <div className="text-sm font-semibold text-slate-900">{user?.full_name}</div>
                <div className="text-xs text-slate-500">Patient</div>
              </div>
            </div>
          </div>
        </header>

        <div className="p-4 lg:p-8 max-w-7xl mx-auto">
          {/* Welcome */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
            <h2 className="text-2xl font-bold text-slate-900">Welcome back, {user?.full_name?.split(" ")[0]}! 👋</h2>
            <p className="text-slate-500 mt-1">Here&apos;s your health overview</p>
          </motion.div>

          {/* Stats Cards */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            {[
              { label: "Health Score", value: `${healthScore}/100`, icon: Heart, color: "blue", trend: "+5%" },
              { label: "Total Analyses", value: String(analyses.length), icon: Brain, color: "purple", trend: "+2 this week" },
              { label: "Reports", value: String(reports.length), icon: FileText, color: "emerald", trend: "Latest today" },
              { label: "Appointments", value: "3", icon: Calendar, color: "orange", trend: "Next: Tomorrow" },
            ].map((stat, i) => (
              <motion.div key={stat.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
                className="bg-white rounded-2xl border border-slate-200 p-5 hover:shadow-lg hover:shadow-slate-200/50 transition-all">
                <div className="flex items-center justify-between mb-3">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${stat.color === "blue" ? "bg-blue-100" : stat.color === "purple" ? "bg-purple-100" : stat.color === "emerald" ? "bg-emerald-100" : "bg-orange-100"}`}>
                    <stat.icon className={`w-5 h-5 ${stat.color === "blue" ? "text-blue-600" : stat.color === "purple" ? "text-purple-600" : stat.color === "emerald" ? "text-emerald-600" : "text-orange-600"}`} />
                  </div>
                  <span className="text-xs text-green-600 font-medium bg-green-50 px-2 py-0.5 rounded-full">{stat.trend}</span>
                </div>
                <div className="text-2xl font-bold text-slate-900">{stat.value}</div>
                <div className="text-sm text-slate-500">{stat.label}</div>
              </motion.div>
            ))}
          </div>

          <div className="grid lg:grid-cols-3 gap-6">
            {/* Recent Analyses */}
            <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 overflow-hidden">
              <div className="p-5 border-b border-slate-100 flex items-center justify-between">
                <h3 className="font-bold text-slate-900">Recent Analyses</h3>
                <Link href="/dashboard/analysis" className="text-sm font-medium text-blue-600 hover:text-blue-700 flex items-center gap-1">
                  New Analysis <ChevronRight className="w-4 h-4" />
                </Link>
              </div>
              {loading ? (
                <div className="p-8 text-center text-slate-400">Loading...</div>
              ) : analyses.length === 0 ? (
                <div className="p-8 text-center">
                  <Brain className="w-12 h-12 text-slate-300 mx-auto mb-3" />
                  <p className="text-slate-500 mb-4">No analyses yet. Upload your first medical image!</p>
                  <Link href="/dashboard/analysis" className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold rounded-xl text-sm">
                    <Upload className="w-4 h-4" /> Upload Image
                  </Link>
                </div>
              ) : (
                <div className="divide-y divide-slate-100">
                  {analyses.map((a) => (
                    <div key={a.id} className="p-4 hover:bg-slate-50 transition-colors flex items-center gap-4">
                      <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-white text-sm font-bold`} style={{ background: riskColor(a.risk_level) }}>
                        {a.image_type.charAt(0).toUpperCase()}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-semibold text-slate-900 truncate">{a.original_filename}</div>
                        <div className="text-xs text-slate-500">{a.image_type.toUpperCase()} • {new Date(a.created_at).toLocaleDateString()}</div>
                      </div>
                      <div className="text-right">
                        <div className={`text-xs font-semibold px-2.5 py-1 rounded-full`} style={{ background: `${riskColor(a.risk_level)}15`, color: riskColor(a.risk_level) }}>
                          {a.risk_level.toUpperCase()}
                        </div>
                        <div className="text-xs text-slate-500 mt-1">{(a.confidence_score * 100).toFixed(1)}% conf.</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Right Column */}
            <div className="space-y-6">
              {/* AI Quick Actions */}
              <div className="bg-white rounded-2xl border border-slate-200 p-5">
                <h3 className="font-bold text-slate-900 mb-4">Quick Actions</h3>
                <div className="space-y-2.5">
                  <Link href="/dashboard/analysis" className="flex items-center gap-3 p-3 rounded-xl bg-blue-50 hover:bg-blue-100 transition-colors group">
                    <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white"><Upload className="w-5 h-5" /></div>
                    <div><div className="text-sm font-semibold text-slate-900">Upload Image</div><div className="text-xs text-slate-500">ECG, MRI, CT, X-Ray</div></div>
                    <ChevronRight className="w-4 h-4 text-slate-400 ml-auto group-hover:text-blue-600" />
                  </Link>
                  <Link href="/dashboard/chatbot" className="flex items-center gap-3 p-3 rounded-xl bg-cyan-50 hover:bg-cyan-100 transition-colors group">
                    <div className="w-10 h-10 rounded-xl bg-cyan-600 flex items-center justify-center text-white"><MessageSquare className="w-5 h-5" /></div>
                    <div><div className="text-sm font-semibold text-slate-900">Talk to AI</div><div className="text-xs text-slate-500">Medical chatbot</div></div>
                    <ChevronRight className="w-4 h-4 text-slate-400 ml-auto group-hover:text-cyan-600" />
                  </Link>
                  <Link href="/dashboard/reports" className="flex items-center gap-3 p-3 rounded-xl bg-emerald-50 hover:bg-emerald-100 transition-colors group">
                    <div className="w-10 h-10 rounded-xl bg-emerald-600 flex items-center justify-center text-white"><FileText className="w-5 h-5" /></div>
                    <div><div className="text-sm font-semibold text-slate-900">View Reports</div><div className="text-xs text-slate-500">{reports.length} reports</div></div>
                    <ChevronRight className="w-4 h-4 text-slate-400 ml-auto group-hover:text-emerald-600" />
                  </Link>
                </div>
              </div>

              {/* Notifications */}
              <div className="bg-white rounded-2xl border border-slate-200 p-5">
                <h3 className="font-bold text-slate-900 mb-4">Notifications</h3>
                {notifications.length === 0 ? (
                  <div className="text-center py-6"><CheckCircle className="w-10 h-10 text-green-400 mx-auto mb-2" /><p className="text-sm text-slate-500">All caught up!</p></div>
                ) : (
                  <div className="space-y-3">
                    {notifications.slice(0, 4).map((n) => (
                      <div key={n.id} className="flex items-start gap-3 p-2.5 rounded-xl hover:bg-slate-50">
                        <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${n.priority === "high" ? "bg-red-100" : "bg-blue-100"}`}>
                          {n.priority === "high" ? <AlertTriangle className="w-4 h-4 text-red-600" /> : <Bell className="w-4 h-4 text-blue-600" />}
                        </div>
                        <div><div className="text-sm font-medium text-slate-900">{n.title}</div><div className="text-xs text-slate-500">{n.message}</div></div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Health Tip */}
              <div className="bg-gradient-to-br from-blue-600 to-cyan-500 rounded-2xl p-5 text-white">
                <div className="text-sm font-semibold opacity-80 mb-1">💡 Health Tip</div>
                <p className="text-sm leading-relaxed">Regular ECG screening can detect heart conditions early. Upload your ECG for a free AI analysis.</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
