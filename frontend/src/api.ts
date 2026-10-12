

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8080"
).replace(/\/$/, "");

export interface CreateUserData {
  name: string;
  email: string;
  income_amount: number;
  income_frequency: string;
  household_size: number;
  location: string;
  preferred_language?: string;
}

export interface UserResponse {
  id: string;
  name: string;
  email: string;
  income_amount: string;
  income_frequency: string;
  household_size: number;
  location: string;
  preferred_language: string;
}

async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);
    const message =
      errorBody?.detail || `Request failed with status ${response.status}`;

    throw new Error(
      typeof message === "string" ? message : JSON.stringify(message),
    );
  }

  return response.json() as Promise<T>;
}

export function checkApiHealth() {
  return apiRequest<{ status: string }>("/health");
}

export function createUser(data: CreateUserData) {
  return apiRequest<UserResponse>("/users", {
    method: "POST",
    body: JSON.stringify({
      ...data,
      preferred_language: data.preferred_language ?? "en",
    }),
  });
}



export interface FoodBudgetResponse {
  id: string;
  user_id: string;
  income_amount: string;
  recommended_amount: string;
  budget_amount: string;
  period: string;
}


export function createFoodBudget(userId: string) {
  return apiRequest<FoodBudgetResponse>("/budgets", {
    method: "POST",
    body: JSON.stringify({
      user_id: userId,
    }),
  });
}


export function getFoodBudget(userId: string) {
  return apiRequest<FoodBudgetResponse | null>(
    `/budgets/user/${encodeURIComponent(userId)}`,
  );
}

export function updateFoodBudget(
  userId: string,
  budgetAmount: number,
) {
  return apiRequest<FoodBudgetResponse>(
    `/budgets/user/${encodeURIComponent(userId)}`,
    {
      method: 'PUT',
      body: JSON.stringify({
        budget_amount: budgetAmount,
      }),
    },
  );
}



export type ContributionFrequency = 'daily' | 'weekly' | 'monthly'

export interface SavingsGoalCreate {
  user_id: string
  name: string
  target_amount: number
  duration_months: number
  contribution_frequency: ContributionFrequency
}

export interface SavingsGoalResponse {
  id: string
  user_id: string
  name: string
  target_amount: string
  current_amount: string
  duration_months: number
  contribution_frequency: ContributionFrequency
  contribution_amount: string
  status: string
}

export interface SavingsProgressResponse {
  goal_id: string
  goal_name: string
  target_amount: string
  current_amount: string
  remaining_amount: string
  progress_percentage: string
  status: string
}

export interface SavingsContributionResponse extends SavingsProgressResponse {
  contribution_amount: string
}

export function createSavingsGoal(data: SavingsGoalCreate) {
  return apiRequest<SavingsGoalResponse>('/savings', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}


export function getSavingsGoals(userId: string) {
  return apiRequest<SavingsGoalResponse[]>(
    `/savings/user/${encodeURIComponent(userId)}`,
  )
}


export function getSavingsProgress(goalId: string) {
  return apiRequest<SavingsProgressResponse>(
    `/savings/${goalId}/progress`,
  )
}

export function addSavingsContribution(
  goalId: string,
  amount: number,
) {
  return apiRequest<SavingsContributionResponse>(
    `/savings/${goalId}/contributions`,
    {
      method: 'POST',
      body: JSON.stringify({ amount }),
    },
  )
}

export interface FoodPlanResponse {
  user_id: string
  income_amount: string | number
  household_size: number
  recommended_food_budget: string | number
  recommended_package: {
    name: string
    estimated_cost: string | number
    duration_days: number
    [key: string]: unknown
  }
  reason: string
}

export interface FoodAssistantChatResponse {
  message: string
  food_plan: FoodPlanResponse
}

export function sendFoodAssistantMessage(
  userId: string,
  message: string,
) {
  return apiRequest<FoodAssistantChatResponse>('/assistant/chat', {
    method: 'POST',
    body: JSON.stringify({
      user_id: userId,
      message,
    }),
  })
}