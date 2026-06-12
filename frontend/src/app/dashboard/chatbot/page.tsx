"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Send, Bot, User, Loader2, Plus, MessageSquare, Trash2,
  Globe, Mic, Volume2, Sparkles
} from "lucide-react";
import { chatbotAPI } from "@/lib/api";
import type { ChatMessage, ChatSession } from "@/types";
import toast from "react-hot-toast";

const SUGGESTED_PROMPTS = [
  "What are the symptoms of heart disease?",
  "How can I prevent heart disease?",
  "Explain my ECG report",
  "What does high cholesterol mean?",
  "What is normal blood pressure?",
  "How to maintain a healthy heart?",
];

export default function ChatbotPage() {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSession, setActiveSession] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadSessions();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const loadSessions = async () => {
    try {
      const res = await chatbotAPI.getSessions();
      setSessions(res.data);
      if (res.data.length > 0 && !activeSession) {
        setActiveSession(res.data[0].id);
        loadMessages(res.data[0].id);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const loadMessages = async (sessionId: string) => {
    try {
      const res = await chatbotAPI.getMessages(sessionId);
      setMessages(res.data);
    } catch (e) {
      console.error(e);
    }
  };

  const createSession = async () => {
    setCreating(true);
    try {
      const res = await chatbotAPI.createSession();
      setSessions((prev) => [res.data, ...prev]);
      setActiveSession(res.data.id);
      setMessages([]);
      toast.success("New chat started!");
    } catch (e) {
      toast.error("Failed to create chat");
    } finally {
      setCreating(false);
    }
  };

  const sendMessage = async (content?: string) => {
    const text = content || input.trim();
    if (!text || loading) return;

    if (!activeSession) {
      await createSession();
      return;
    }

    setInput("");
    setLoading(true);

    // Optimistic user message
    const tempMsg: ChatMessage = {
      id: "temp-" + Date.now(),
      session_id: activeSession,
      role: "user",
      content: text,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempMsg]);

    try {
      const res = await chatbotAPI.sendMessage(text, activeSession);
      setMessages((prev) => [...prev.filter((m) => m.id !== tempMsg.id), res.data]);
    } catch (e) {
      toast.error("Failed to send message");
      setMessages((prev) => prev.filter((m) => m.id !== tempMsg.id));
    } finally {
      setLoading(false);
    }
  };

  const deleteSession = async (sessionId: string) => {
    try {
      await chatbotAPI.deleteSession(sessionId);
      setSessions((prev) => prev.filter((s) => s.id !== sessionId));
      if (activeSession === sessionId) {
        setActiveSession(null);
        setMessages([]);
      }
      toast.success("Chat deleted");
    } catch (e) {
      toast.error("Failed to delete");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar — Sessions */}
      <aside className="w-72 bg-white border-r border-slate-200 flex flex-col hidden md:flex">
        <div className="p-4 border-b border-slate-100">
          <button
            onClick={createSession}
            disabled={creating}
            className="w-full py-2.5 bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold rounded-xl text-sm flex items-center justify-center gap-2 hover:shadow-lg transition-all disabled:opacity-50"
          >
            {creating ? <Loader2 className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
            New Chat
          </button>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {sessions.map((session) => (
            <div
              key={session.id}
              onClick={() => { setActiveSession(session.id); loadMessages(session.id); }}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-xl cursor-pointer transition-all group ${
                activeSession === session.id ? "bg-blue-50 text-blue-700" : "hover:bg-slate-50 text-slate-600"
              }`}
            >
              <MessageSquare className="w-4 h-4 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium truncate">{session.title || "New Chat"}</div>
                <div className="text-xs text-slate-400">{session.message_count} messages</div>
              </div>
              <button
                onClick={(e) => { e.stopPropagation(); deleteSession(session.id); }}
                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-50 rounded-lg transition-all"
              >
                <Trash2 className="w-3.5 h-3.5 text-red-400" />
              </button>
            </div>
          ))}
          {sessions.length === 0 && (
            <div className="text-center py-8 text-slate-400 text-sm">No chats yet</div>
          )}
        </div>
        <div className="p-3 border-t border-slate-100">
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <Globe className="w-3.5 h-3.5" />
            <span>English • Telugu • Hindi • Tamil</span>
          </div>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="bg-white border-b border-slate-200 px-4 lg:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-600 to-cyan-500 flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-sm font-bold text-slate-900">AI Medical Assistant</h1>
              <p className="text-xs text-slate-500">Powered by BioGPT & BioBERT</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button className="p-2 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors" title="Voice input">
              <Mic className="w-5 h-5" />
            </button>
            <button className="p-2 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors" title="Text to speech">
              <Volume2 className="w-5 h-5" />
            </button>
          </div>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 lg:p-6 space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-600 to-cyan-500 flex items-center justify-center mx-auto mb-4">
                <Sparkles className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-xl font-bold text-slate-900 mb-2">How can I help you today?</h2>
              <p className="text-slate-500 mb-6 max-w-md mx-auto">I can help explain medical reports, discuss heart health, and answer health-related questions.</p>
              <div className="grid sm:grid-cols-2 gap-2 max-w-lg mx-auto">
                {SUGGESTED_PROMPTS.map((prompt) => (
                  <button
                    key={prompt}
                    onClick={() => sendMessage(prompt)}
                    className="text-left p-3 rounded-xl border border-slate-200 text-sm text-slate-600 hover:border-blue-300 hover:bg-blue-50 transition-all"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex gap-3 ${msg.role === "user" ? "flex-row-reverse" : ""}`}
            >
              <div className={`w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 ${
                msg.role === "user" ? "bg-slate-200" : "bg-gradient-to-br from-blue-600 to-cyan-500"
              }`}>
                {msg.role === "user" ? <User className="w-4 h-4 text-slate-600" /> : <Bot className="w-4 h-4 text-white" />}
              </div>
              <div className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                msg.role === "user"
                  ? "bg-blue-600 text-white rounded-tr-md"
                  : "bg-white border border-slate-200 text-slate-700 rounded-tl-md"
              }`}>
                {msg.content}
              </div>
            </motion.div>
          ))}

          {loading && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-600 to-cyan-500 flex items-center justify-center">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <div className="bg-white border border-slate-200 rounded-2xl rounded-tl-md px-4 py-3">
                <div className="flex gap-1.5">
                  <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="p-4 bg-white border-t border-slate-200">
          <div className="max-w-3xl mx-auto flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              placeholder="Ask a health question..."
              className="flex-1 px-4 py-3 rounded-xl border border-slate-200 bg-slate-50 text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
            />
            <button
              onClick={() => sendMessage()}
              disabled={!input.trim() || loading}
              className="px-5 py-3 bg-gradient-to-r from-blue-600 to-cyan-500 text-white rounded-xl hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          <p className="text-center text-xs text-slate-400 mt-2">AI-generated information is for educational purposes only. Always consult a healthcare professional.</p>
        </div>
      </main>
    </div>
  );
}
