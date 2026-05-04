import api from "./client";

type SignupPayload = {
  email: string;
  full_name: string;
  password: string;
};

type LoginPayload = {
  email: string;
  password: string;
};

export async function signup(payload: SignupPayload) {
  const res = await api.post("/api/auth/signup", payload);
  return res.data;
}

export async function login(payload: LoginPayload) {
  const res = await api.post("/api/auth/login", payload);
  return res.data as { access_token: string; token_type: string };
}

export async function getMe() {
  const res = await api.get("/api/auth/me");
  return res.data;
}
