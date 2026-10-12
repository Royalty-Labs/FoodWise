
import { useEffect, useState, type FormEvent } from 'react'
import {
  LayoutDashboard,
  CalendarDays,
  PiggyBank,
  Wallet,
  Leaf,
  ArrowUpRight,
  Plus,
  ShoppingBasket,
  Utensils,
  TrendingUp,
  CircleDollarSign,
  CheckCircle2,
  Clock3,
  Sprout,
  Target,
  ChevronRight,
  X,
  MessageCircle,
  Send,
  Sparkles,
} from 'lucide-react'
import './App.css'
import {
  createUser,
  createFoodBudget,
  getFoodBudget,
  updateFoodBudget,
  createSavingsGoal,
  getSavingsGoals,
  sendFoodAssistantMessage,
  addSavingsContribution,
  type UserResponse,
  type FoodBudgetResponse,
  type SavingsGoalResponse,
  type FoodAssistantChatResponse,
} from './api'

type Tab =
  | 'Overview'
  | 'Food Planner'
  | 'My Savings'
  | 'Food Budget'
  | 'AI Food Assistant'

type MealPlan = {
  id: number
  name: string
  day: string
  meal: string
}

const navigation: { label: Tab; icon: typeof LayoutDashboard }[] = [
  { label: 'Overview', icon: LayoutDashboard },
  { label: 'Food Planner', icon: CalendarDays },
  { label: 'My Savings', icon: PiggyBank },
  { label: 'Food Budget', icon: Wallet },
  { label: 'AI Food Assistant', icon: MessageCircle },
]

const money = (amount: number) =>
  new Intl.NumberFormat('en-NG', {
    style: 'currency',
    currency: 'NGN',
    maximumFractionDigits: 0,
  }).format(Number.isFinite(amount) ? amount : 0)

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('Overview')
  const [budget, setBudget] = useState('')
  const [savedAmount, setSavedAmount] = useState('')
  const [savingsTarget, setSavingsTarget] = useState('')
  const [mealName, setMealName] = useState('')
  const [mealDay, setMealDay] = useState('Monday')
  const [mealType, setMealType] = useState('Lunch')
  const [mealPlans, setMealPlans] = useState<MealPlan[]>([])
  const [notice, setNotice] = useState('')

  const [assistantInput, setAssistantInput] = useState('')
  const [assistantMessages, setAssistantMessages] = useState<
    { role: 'user' | 'assistant'; content: string }[]
  >([])
  const [assistantResponse, setAssistantResponse] =
    useState<FoodAssistantChatResponse | null>(null)
  const [isAssistantLoading, setIsAssistantLoading] = useState(false)
  const [assistantError, setAssistantError] = useState('')

  const [user, setUser] = useState<UserResponse | null>(() => {
    const storedUser = localStorage.getItem('foodwise_user')

    if (!storedUser) return null

    try {
      return JSON.parse(storedUser) as UserResponse
    } catch {
      return null
    }
  })

  const [registerName, setRegisterName] = useState('')
  const [registerEmail, setRegisterEmail] = useState('')
  const [monthlyIncome, setMonthlyIncome] = useState('')
  const [householdSize, setHouseholdSize] = useState('1')
  const [registerLocation, setRegisterLocation] = useState('')
  const [isRegistering, setIsRegistering] = useState(false)
  const [registrationError, setRegistrationError] = useState('')

  const [recommendedBudget, setRecommendedBudget] =
    useState<FoodBudgetResponse | null>(null)
  const [isCreatingBudget, setIsCreatingBudget] = useState(false)
  const [budgetError, setBudgetError] = useState('')

  const [goalName, setGoalName] = useState('My food fund')
  const [goalDuration, setGoalDuration] = useState('3')
  const [contributionFrequency, setContributionFrequency] =
    useState<'daily' | 'weekly' | 'monthly'>('weekly')

  const [activeGoal, setActiveGoal] =
    useState<SavingsGoalResponse | null>(null)
  const [savingsGoals, setSavingsGoals] =
    useState<SavingsGoalResponse[]>([])
  const [isLoadingGoals, setIsLoadingGoals] = useState(false)
  const [isSavingGoal, setIsSavingGoal] = useState(false)
  const [isAddingContribution, setIsAddingContribution] = useState(false)
  const [savingsError, setSavingsError] = useState('')

  async function handleAssistantSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    const message = assistantInput.trim()

    if (!message || !user || isAssistantLoading) return

    setAssistantMessages((current) => [
      ...current,
      { role: 'user', content: message },
    ])
    setAssistantInput('')
    setAssistantError('')
    setAssistantResponse(null)
    setIsAssistantLoading(true)

    try {
      const result = await sendFoodAssistantMessage(user.id, message)

      setAssistantResponse(result)
      setAssistantMessages((current) => [
        ...current,
        { role: 'assistant', content: result.message },
      ])
    } catch (error) {
      setAssistantError(
        error instanceof Error
          ? error.message
          : 'The assistant could not respond. Please try again.',
      )
    } finally {
      setIsAssistantLoading(false)
    }
  }

  // Load the signed-in user's existing savings goals.
  useEffect(() => {
    const currentUser = user

    if (!currentUser) {
      setSavingsGoals([])
      setActiveGoal(null)
      setIsLoadingGoals(false)
      return
    }

    let cancelled = false

    async function loadSavingsGoals() {
      setIsLoadingGoals(true)
      setSavingsError('')

      try {
        const goals = await getSavingsGoals(user!.id)

        if (cancelled) return

        setSavingsGoals(goals)

        setActiveGoal((current) => {
          if (current) {
            return (
              goals.find((goal) => goal.id === current.id) ??
              goals[0] ??
              null
            )
          }

          return goals[0] ?? null
        })
      } catch (error) {
        if (!cancelled) {
          setSavingsError(
            error instanceof Error
              ? error.message
              : 'Could not load your savings goals.',
          )
        }
      } finally {
        if (!cancelled) {
          setIsLoadingGoals(false)
        }
      }
    }

    void loadSavingsGoals()

    return () => {
      cancelled = true
    }
  }, [user])

  // Load the signed-in user's saved food budget.
  useEffect(() => {
    const currentUser = user

    if (!currentUser) {
      setBudget('')
      setRecommendedBudget(null)
      setBudgetError('')
      return
    }

    let cancelled = false

    async function loadBudget() {
      try {
        const result = await getFoodBudget(user!.id)

        if (cancelled) return

        if (result) {
          setRecommendedBudget(result)
          setBudget(result.budget_amount)
        } else {
          setRecommendedBudget(null)
          setBudget('')
        }
      } catch (error) {
        if (cancelled) return

        setBudgetError(
          error instanceof Error
            ? error.message
            : 'Could not load your saved food budget.',
        )
      }
    }

    void loadBudget()

    return () => {
      cancelled = true
    }
  }, [user])

  const budgetValue = Math.max(0, Number(budget) || 0)

  const savedValue = activeGoal
    ? Number(activeGoal.current_amount) || 0
    : 0

  const targetValue = activeGoal
    ? Number(activeGoal.target_amount) || 0
    : Math.max(0, Number(savingsTarget) || 0)

  const savingsProgress =
    targetValue > 0
      ? Math.min(100, (savedValue / targetValue) * 100)
      : 0

  function addMeal(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    if (!mealName.trim()) return

    setMealPlans((current) => [
      ...current,
      {
        id: Date.now(),
        name: mealName.trim(),
        day: mealDay,
        meal: mealType,
      },
    ])

    setMealName('')
    setNotice('Your meal has been added to your plan.')
  }

  function removeMeal(id: number) {
    setMealPlans((current) => current.filter((meal) => meal.id !== id))
    setNotice('Meal removed from your plan.')
  }

  async function saveBudget(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    if (!user) {
      setBudgetError('Please create or select a user first.')
      return
    }

    const amount = Number(budget)

    if (!Number.isFinite(amount) || amount < 0) {
      setBudgetError('Enter a valid budget amount.')
      return
    }

    setBudgetError('')

    try {
      const result = await updateFoodBudget(user.id, amount)

      setRecommendedBudget(result)
      setBudget(result.budget_amount)
      setNotice('Your food budget has been saved.')
    } catch (error) {
      setBudgetError(
        error instanceof Error
          ? error.message
          : 'Could not save your food budget.',
      )
    }
  }

  async function handleCreateBudget() {
    if (!user) return

    setBudgetError('')
    setIsCreatingBudget(true)

    try {
      const result = await createFoodBudget(user.id)

      setRecommendedBudget(result)
      setBudget(result.budget_amount)
      setNotice('Your recommended monthly food budget is ready.')
    } catch (error) {
      setBudgetError(
        error instanceof Error
          ? error.message
          : 'Could not create your food budget.',
      )
    } finally {
      setIsCreatingBudget(false)
    }
  }

  async function handleCreateSavingsGoal(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()
    setSavingsError('')
    setNotice('')

    if (!user) {
      setSavingsError('Please register before creating a savings goal.')
      return
    }

    const target = Number(savingsTarget)
    const duration = Number(goalDuration)

    if (!goalName.trim() || goalName.trim().length < 2) {
      setSavingsError('Enter a goal name with at least two characters.')
      return
    }

    if (!Number.isFinite(target) || target <= 0) {
      setSavingsError('Enter a target amount greater than zero.')
      return
    }

    if (!Number.isInteger(duration) || duration < 1) {
      setSavingsError('Duration must be at least one whole month.')
      return
    }

    setIsSavingGoal(true)

    try {
      const goal = await createSavingsGoal({
        user_id: user.id,
        name: goalName.trim(),
        target_amount: target,
        duration_months: duration,
        contribution_frequency: contributionFrequency,
      })

      setSavingsGoals((current) => [
        goal,
        ...current.filter((item) => item.id !== goal.id),
      ])

      setActiveGoal(goal)
      setSavedAmount('')
      setSavingsTarget(String(goal.target_amount))
      setGoalName('My food fund')
      setGoalDuration('3')
      setContributionFrequency('weekly')
      setNotice('Your savings goal has been saved to FoodWise.')
    } catch (error) {
      setSavingsError(
        error instanceof Error
          ? error.message
          : 'Could not create your savings goal.',
      )
    } finally {
      setIsSavingGoal(false)
    }
  }

  async function handleAddContribution(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()
    setSavingsError('')
    setNotice('')

    if (!activeGoal) {
      setSavingsError(
        'Select a savings goal before recording a contribution.',
      )
      return
    }

    const amount = Number(savedAmount)

    if (!Number.isFinite(amount) || amount <= 0) {
      setSavingsError('Enter a contribution greater than zero.')
      return
    }

    if (activeGoal.status === 'completed') {
      setSavingsError(
        'This goal is already complete. Select or create another goal.',
      )
      return
    }

    setIsAddingContribution(true)

    try {
      const result = await addSavingsContribution(activeGoal.id, amount)

      setActiveGoal((current) =>
        current && current.id === result.goal_id
          ? {
              ...current,
              current_amount: result.current_amount,
              status: result.status,
            }
          : current,
      )

      setSavingsGoals((current) =>
        current.map((goal) =>
          goal.id === result.goal_id
            ? {
                ...goal,
                current_amount: result.current_amount,
                status: result.status,
              }
            : goal,
        ),
      )

      setSavedAmount('')
      setNotice(
        result.status === 'completed'
          ? 'Congratulations! Your savings goal is complete.'
          : 'Your contribution has been recorded.',
      )
    } catch (error) {
      setSavingsError(
        error instanceof Error
          ? error.message
          : 'Could not record your contribution. Please try again.',
      )
    } finally {
      setIsAddingContribution(false)
    }
  }

  async function handleRegistration(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setRegistrationError('')

    const income = Number(monthlyIncome)
    const household = Number(householdSize)

    if (!Number.isFinite(income) || income <= 0) {
      setRegistrationError('Enter a monthly income greater than zero.')
      return
    }

    if (!Number.isInteger(household) || household < 1) {
      setRegistrationError('Household size must be at least one.')
      return
    }

    setIsRegistering(true)

    try {
      const createdUser = await createUser({
        name: registerName.trim(),
        email: registerEmail.trim(),
        income_amount: income,
        income_frequency: 'monthly',
        household_size: household,
        location: registerLocation.trim(),
        preferred_language: 'en',
      })

      localStorage.setItem('foodwise_user', JSON.stringify(createdUser))
      setUser(createdUser)
      setNotice(`Welcome to FoodWise, ${createdUser.name}!`)
    } catch (error) {
      setRegistrationError(
        error instanceof Error
          ? error.message
          : 'Registration failed. Please try again.',
      )
    } finally {
      setIsRegistering(false)
    }
  }

  function navigate(tab: Tab) {
    setActiveTab(tab)
    setNotice('')
  }

  function selectSavingsGoal(goal: SavingsGoalResponse) {
    setActiveGoal(goal)
    setSavingsTarget(String(goal.target_amount))
    setSavedAmount('')
    setSavingsError('')
    setNotice('')
  }

  function startNewSavingsGoal() {
    setActiveGoal(null)
    setSavingsTarget('')
    setSavedAmount('')
    setSavingsError('')
    setGoalName('My food fund')
    setGoalDuration('3')
    setContributionFrequency('weekly')
    setNotice('')
  }

  if (!user) {
    return (
      <div className="registration-screen">
        <div className="registration-card">
          <div className="registration-brand">
            <span className="brand-mark">
              <Leaf size={24} />
            </span>
            <span>FoodWise</span>
          </div>

          <p className="eyebrow">YOUR FOOD, YOUR PLAN</p>
          <h1>Let's make food planning easier.</h1>
          <p className="registration-description">
            Tell us a little about yourself so we can help you plan
            your food budget and savings goals.
          </p>

          <form className="registration-form" onSubmit={handleRegistration}>
            <label>
              Full name
              <input
                type="text"
                value={registerName}
                onChange={(event) => setRegisterName(event.target.value)}
                placeholder="Your full name"
                minLength={2}
                maxLength={100}
                required
              />
            </label>

            <label>
              Email address
              <input
                type="email"
                value={registerEmail}
                onChange={(event) => setRegisterEmail(event.target.value)}
                placeholder="you@example.com"
                required
              />
            </label>

            <label>
              Monthly income (₦)
              <input
                type="number"
                value={monthlyIncome}
                onChange={(event) => setMonthlyIncome(event.target.value)}
                placeholder="150000"
                min="0.01"
                step="0.01"
                required
              />
            </label>

            <label>
              Household size
              <input
                type="number"
                value={householdSize}
                onChange={(event) => setHouseholdSize(event.target.value)}
                min="1"
                step="1"
                required
              />
            </label>

            <label>
              Location
              <input
                type="text"
                value={registerLocation}
                onChange={(event) => setRegisterLocation(event.target.value)}
                placeholder="City or town"
                required
              />
            </label>

            {registrationError && (
              <p className="registration-error" role="alert">
                {registrationError}
              </p>
            )}

            <button
              className="primary-button registration-submit"
              type="submit"
              disabled={isRegistering}
            >
              {isRegistering ? 'Creating your account...' : 'Get started'}
              {!isRegistering && <ArrowUpRight size={17} />}
            </button>
          </form>

          <p className="registration-note">
            Your income is used to calculate a recommended monthly food budget.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="foodwise-app">
      <aside className="sidebar">
        <button
          className="brand brand-button"
          onClick={() => navigate('Overview')}
          aria-label="Go to FoodWise overview"
        >
          <span className="brand-mark">
            <Leaf size={22} />
          </span>
          <span>FoodWise</span>
        </button>

        <p className="brand-caption">Eat well. Plan better.</p>
        <p className="menu-label">YOUR WORKSPACE</p>

        <nav className="navigation" aria-label="Main navigation">
          {navigation.map(({ label, icon: Icon }) => (
            <button
              key={label}
              className={`nav-item ${activeTab === label ? 'active' : ''}`}
              onClick={() => navigate(label)}
              aria-current={activeTab === label ? 'page' : undefined}
            >
              <Icon size={19} strokeWidth={1.9} />
              <span>{label}</span>
              {activeTab === label && <span className="nav-indicator" />}
            </button>
          ))}
        </nav>

        <div className="sidebar-note">
          <div className="note-icon">
            <Sprout size={20} />
          </div>
          <p className="note-label">A LITTLE REMINDER</p>
          <h3>Good food starts with a good plan.</h3>
          <p>
            Small, thoughtful steps can make everyday food decisions easier.
          </p>
        </div>

        <div className="profile">
          <div className="avatar">
            {user.name?.trim().charAt(0).toUpperCase() || 'F'}
          </div>
          <div className="profile-copy">
            <strong>{user.name || 'My FoodWise'}</strong>
            <p>Personal workspace</p>
          </div>
          <span className="profile-status" title="Connected workspace" />
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">YOUR FOOD, YOUR PLAN</p>
            <h1>
              {activeTab === 'Overview'
                ? 'Good to see you!'
                : activeTab}
            </h1>
            <p className="topbar-subtitle">
              {activeTab === 'Overview'
                ? 'A little planning today can go a long way.'
                : activeTab === 'Food Planner'
                  ? 'Plan meals that work for your household.'
                  : activeTab === 'My Savings'
                    ? 'Build a plan for the food you need.'
                    : activeTab === 'AI Food Assistant'
                      ? 'Get food planning guidance tailored to your household.'
                      : 'Give your food spending a clear direction.'}
            </p>
          </div>

          <div className="workspace-chip">
            <span className="status-dot" />
            <span>Personal workspace</span>
          </div>
        </header>

        {notice && (
          <div className="notice" role="status">
            <CheckCircle2 size={17} />
            <span>{notice}</span>
            <button
              onClick={() => setNotice('')}
              aria-label="Dismiss notification"
            >
              <X size={16} />
            </button>
          </div>
        )}

        {activeTab === 'Overview' && (
          <>
            <section className="welcome">
              <div className="welcome-copy">
                <span className="welcome-tag">
                  <Sprout size={14} /> YOUR FRESH START
                </span>
                <h2>
                  Make room for <span>better food days.</span>
                </h2>
                <p>
                  Plan your meals, manage your food budget, and work towards
                  your savings goals — all in one place.
                </p>
                <button
                  className="primary-button"
                  onClick={() => navigate('Food Planner')}
                >
                  Plan your meals <ArrowUpRight size={17} />
                </button>
              </div>

              <div className="welcome-visual" aria-hidden="true">
                <div className="visual-orbit orbit-one" />
                <div className="visual-orbit orbit-two" />
                <div className="produce-circle produce-main">
                  <ShoppingBasket size={57} strokeWidth={1.25} />
                </div>
                <div className="produce-bubble bubble-one">
                  <Leaf size={24} />
                </div>
                <div className="produce-bubble bubble-two">
                  <Sprout size={22} />
                </div>
                <span className="visual-caption">
                  Fresh thinking, every day.
                </span>
              </div>

              <div className="hero-decoration" aria-hidden="true">
                ✳
              </div>
            </section>

            <section className="section-heading">
              <div>
                <p className="eyebrow">AT A GLANCE</p>
                <h2>Your food overview</h2>
                <p className="section-description">
                  Your current numbers, all in one place.
                </p>
              </div>
              <span className="local-label">LOCAL PREVIEW</span>
            </section>

            <section className="stats-grid">
              <article className="stat-card">
                <div className="stat-topline">
                  <span className="stat-icon green">
                    <Wallet size={20} />
                  </span>
                  <span className="stat-trend">MONTHLY</span>
                </div>
                <p className="stat-label">Food budget</p>
                <h3>{money(budgetValue)}</h3>
                <button
                  className="text-link"
                  onClick={() => navigate('Food Budget')}
                >
                  Manage budget <ChevronRight size={15} />
                </button>
              </article>

              <article className="stat-card">
                <div className="stat-topline">
                  <span className="stat-icon gold">
                    <PiggyBank size={20} />
                  </span>
                  <span className="stat-trend">SAVINGS</span>
                </div>
                <p className="stat-label">Amount saved</p>
                <h3>{money(savedValue)}</h3>
                <button
                  className="text-link"
                  onClick={() => navigate('My Savings')}
                >
                  View savings <ChevronRight size={15} />
                </button>
              </article>

              <article className="stat-card">
                <div className="stat-topline">
                  <span className="stat-icon coral">
                    <Utensils size={20} />
                  </span>
                  <span className="stat-trend">PLANNING</span>
                </div>
                <p className="stat-label">Meals planned</p>
                <h3>
                  {mealPlans.length}{' '}
                  <span className="stat-unit">
                    {mealPlans.length === 1 ? 'meal' : 'meals'}
                  </span>
                </h3>
                <button
                  className="text-link"
                  onClick={() => navigate('Food Planner')}
                >
                  View meal plan <ChevronRight size={15} />
                </button>
              </article>
            </section>

            <section className="overview-grid">
              <article className="panel">
                <div className="panel-heading">
                  <div>
                    <p className="eyebrow">YOUR NEXT STEPS</p>
                    <h2>Build your food routine</h2>
                    <p className="section-description">
                      Start with one small step at a time.
                    </p>
                  </div>
                  <span className="heading-icon">
                    <CheckCircle2 size={21} />
                  </span>
                </div>

                <button
                  className="action-row"
                  onClick={() => navigate('Food Budget')}
                >
                  <span className="action-icon">
                    <Wallet size={19} />
                  </span>
                  <span className="action-copy">
                    <strong>Set your food budget</strong>
                    <small>Choose a spending amount for the month.</small>
                  </span>
                  <ChevronRight size={18} />
                </button>

                <button
                  className="action-row"
                  onClick={() => navigate('Food Planner')}
                >
                  <span className="action-icon">
                    <CalendarDays size={19} />
                  </span>
                  <span className="action-copy">
                    <strong>Plan what you will eat</strong>
                    <small>Organise meals for the week ahead.</small>
                  </span>
                  <ChevronRight size={18} />
                </button>

                <button
                  className="action-row"
                  onClick={() => navigate('My Savings')}
                >
                  <span className="action-icon">
                    <PiggyBank size={19} />
                  </span>
                  <span className="action-copy">
                    <strong>Create a food savings goal</strong>
                    <small>Give your food savings a purpose.</small>
                  </span>
                  <ChevronRight size={18} />
                </button>
              </article>

              <article className="panel goal-summary">
                <div className="panel-heading">
                  <div>
                    <p className="eyebrow">YOUR PROGRESS</p>
                    <h2>Food savings goal</h2>
                  </div>
                  <span className="heading-icon gold-icon">
                    <Target size={21} />
                  </span>
                </div>

                {targetValue > 0 ? (
                  <>
                    <div className="goal-amount">
                      {money(savedValue)}{' '}
                      <span>of {money(targetValue)}</span>
                    </div>
                    <div className="progress-track">
                      <div
                        className="progress-fill"
                        style={{ width: `${savingsProgress}%` }}
                      />
                    </div>
                    <div className="progress-meta">
                      <span>{Math.round(savingsProgress)}% reached</span>
                      <span>
                        {money(Math.max(0, targetValue - savedValue))} to go
                      </span>
                    </div>
                    <button
                      className="secondary-button"
                      onClick={() => navigate('My Savings')}
                    >
                      View savings goal <ArrowUpRight size={16} />
                    </button>
                  </>
                ) : (
                  <div className="empty-goal">
                    <div className="goal-art">
                      <CircleDollarSign size={37} />
                    </div>
                    <h3>Give your goal a starting point.</h3>
                    <p>
                      Set a target for the food expenses you want to prepare for.
                    </p>
                    <button
                      className="secondary-button"
                      onClick={() => navigate('My Savings')}
                    >
                      Set a savings goal <ArrowUpRight size={16} />
                    </button>
                  </div>
                )}
              </article>
            </section>
          </>
        )}

        {activeTab === 'Food Planner' && (
          <section className="page-layout">
            <div className="page-intro">
              <div>
                <p className="eyebrow">PLAN AHEAD</p>
                <h2>Your meal planner</h2>
                <p className="section-description">
                  Make a simple plan for what you want to eat.
                </p>
              </div>
              <span className="large-page-icon">
                <CalendarDays size={27} />
              </span>
            </div>

            <div className="planner-grid">
              <article className="panel">
                <div className="panel-heading">
                  <div>
                    <h2>Add a meal</h2>
                    <p className="section-description">
                      Add an idea to your weekly plan.
                    </p>
                  </div>
                  <span className="heading-icon">
                    <Plus size={21} />
                  </span>
                </div>

                <form className="app-form" onSubmit={addMeal}>
                  <label htmlFor="meal-name">Meal name</label>
                  <input
                    id="meal-name"
                    value={mealName}
                    onChange={(event) => setMealName(event.target.value)}
                    placeholder="e.g. Rice and beans"
                    required
                  />

                  <div className="form-two-columns">
                    <div>
                      <label htmlFor="meal-day">Day</label>
                      <select
                        id="meal-day"
                        value={mealDay}
                        onChange={(event) => setMealDay(event.target.value)}
                      >
                        {[
                          'Monday',
                          'Tuesday',
                          'Wednesday',
                          'Thursday',
                          'Friday',
                          'Saturday',
                          'Sunday',
                        ].map((day) => (
                          <option key={day}>{day}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label htmlFor="meal-type">Meal</label>
                      <select
                        id="meal-type"
                        value={mealType}
                        onChange={(event) => setMealType(event.target.value)}
                      >
                        {['Breakfast', 'Lunch', 'Dinner', 'Snack'].map(
                          (type) => (
                            <option key={type}>{type}</option>
                          ),
                        )}
                      </select>
                    </div>
                  </div>

                  <button className="primary-button full-button" type="submit">
                    <Plus size={17} /> Add to meal plan
                  </button>
                </form>
              </article>

              <article className="panel meal-list-panel">
                <div className="panel-heading">
                  <div>
                    <h2>Your planned meals</h2>
                    <p className="section-description">
                      {mealPlans.length}{' '}
                      {mealPlans.length === 1 ? 'meal' : 'meals'} added in this
                      session.
                    </p>
                  </div>
                  <span className="heading-icon">
                    <Utensils size={21} />
                  </span>
                </div>

                {mealPlans.length === 0 ? (
                  <div className="empty-state">
                    <div className="empty-state-icon">
                      <ShoppingBasket size={28} />
                    </div>
                    <h3>Your plan starts with one meal.</h3>
                    <p>
                      Add a meal using the form. It will appear here so you can
                      review your plan.
                    </p>
                  </div>
                ) : (
                  <div className="meal-list">
                    {mealPlans.map((meal) => (
                      <div className="meal-row" key={meal.id}>
                        <span className="meal-row-icon">
                          <Utensils size={18} />
                        </span>
                        <div className="meal-row-copy">
                          <strong>{meal.name}</strong>
                          <span>
                            <Clock3 size={13} /> {meal.day} · {meal.meal}
                          </span>
                        </div>
                        <button
                          className="icon-button"
                          type="button"
                          onClick={() => removeMeal(meal.id)}
                          aria-label={`Remove ${meal.name}`}
                        >
                          <X size={17} />
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </article>
            </div>

            <p className="demo-disclaimer">
              Your meal plan is stored in this page's current session only. It
              is not yet saved to your account.
            </p>
          </section>
        )}

        {activeTab === 'My Savings' && (
          <section className="page-layout">
            <div className="page-intro">
              <div>
                <p className="eyebrow">SAVE WITH PURPOSE</p>
                <h2>Your food savings</h2>
                <p className="section-description">
                  Set a target and track the figures you enter.
                </p>
              </div>
              <span className="large-page-icon gold-page-icon">
                <PiggyBank size={27} />
              </span>
            </div>

            <div className="savings-summary-grid">
              <article className="stat-card">
                <span className="stat-icon gold">
                  <PiggyBank size={20} />
                </span>
                <p className="stat-label">Amount saved</p>
                <h3>{money(savedValue)}</h3>
              </article>

              <article className="stat-card">
                <span className="stat-icon green">
                  <Target size={20} />
                </span>
                <p className="stat-label">Savings target</p>
                <h3>{money(targetValue)}</h3>
              </article>

              <article className="stat-card">
                <span className="stat-icon coral">
                  <TrendingUp size={20} />
                </span>
                <p className="stat-label">Target progress</p>
                <h3>{Math.round(savingsProgress)}%</h3>
              </article>
            </div>

            {isLoadingGoals && (
              <p className="section-description" role="status">
                Loading your savings goals...
              </p>
            )}

            {savingsGoals.length > 0 && (
              <section className="panel">
                <div className="panel-heading">
                  <div>
                    <h2>Your savings goals</h2>
                    <p className="section-description">
                      Select a goal to view its progress and record a
                      contribution.
                    </p>
                  </div>
                </div>

                <div className="app-form">
                  {savingsGoals.map((goal) => (
                    <button
                      key={goal.id}
                      type="button"
                      className="text-link"
                      aria-pressed={activeGoal?.id === goal.id}
                      onClick={() => selectSavingsGoal(goal)}
                    >
                      {goal.name} — {money(Number(goal.current_amount))} of{' '}
                      {money(Number(goal.target_amount))}
                      {activeGoal?.id === goal.id ? ' (Selected)' : ''}
                    </button>
                  ))}
                </div>
              </section>
            )}

            <div className="savings-layout">
              <article className="panel">
                <div className="panel-heading">
                  <div>
                    <h2>
                      {activeGoal
                        ? activeGoal.name
                        : 'Create a savings goal'}
                    </h2>
                    <p className="section-description">
                      {activeGoal
                        ? 'Your goal is connected to the FoodWise backend.'
                        : 'Set a target and choose how often you plan to contribute.'}
                    </p>
                  </div>
                </div>

                {!activeGoal ? (
                  <form
                    className="app-form"
                    onSubmit={handleCreateSavingsGoal}
                  >
                    <label htmlFor="goal-name">Goal name</label>
                    <input
                      id="goal-name"
                      value={goalName}
                      onChange={(event) => setGoalName(event.target.value)}
                      minLength={2}
                      maxLength={100}
                      required
                      placeholder="e.g. Monthly food fund"
                    />

                    <label htmlFor="savings-target">Target amount (₦)</label>
                    <input
                      id="savings-target"
                      type="number"
                      min="1"
                      step="1"
                      value={savingsTarget}
                      onChange={(event) =>
                        setSavingsTarget(event.target.value)
                      }
                      required
                      placeholder="e.g. 50000"
                    />

                    <label htmlFor="goal-duration">Duration (months)</label>
                    <input
                      id="goal-duration"
                      type="number"
                      min="1"
                      step="1"
                      value={goalDuration}
                      onChange={(event) =>
                        setGoalDuration(event.target.value)
                      }
                      required
                    />

                    <label htmlFor="contribution-frequency">
                      Contribution frequency
                    </label>
                    <select
                      id="contribution-frequency"
                      value={contributionFrequency}
                      onChange={(event) =>
                        setContributionFrequency(
                          event.target.value as
                            | 'daily'
                            | 'weekly'
                            | 'monthly',
                        )
                      }
                    >
                      <option value="daily">Daily</option>
                      <option value="weekly">Weekly</option>
                      <option value="monthly">Monthly</option>
                    </select>

                    <button
                      className="primary-button full-button"
                      type="submit"
                      disabled={isSavingGoal}
                    >
                      {isSavingGoal ? 'Creating goal...' : 'Create savings goal'}
                      {!isSavingGoal && <ArrowUpRight size={17} />}
                    </button>
                  </form>
                ) : (
                  <>
                    <p>
                      Target: {money(Number(activeGoal.target_amount))}
                    </p>
                    <p>
                      Planned contribution:{' '}
                      {money(Number(activeGoal.contribution_amount))}{' '}
                      {activeGoal.contribution_frequency}
                    </p>
                    <p>Duration: {activeGoal.duration_months} months</p>
                    <p>Status: {activeGoal.status}</p>

                    <form
                      className="app-form"
                      onSubmit={handleAddContribution}
                    >
                      <label htmlFor="saved-amount">
                        Contribution amount (₦)
                      </label>
                      <input
                        id="saved-amount"
                        type="number"
                        min="1"
                        step="1"
                        value={savedAmount}
                        onChange={(event) =>
                          setSavedAmount(event.target.value)
                        }
                        required
                        placeholder="e.g. 1000"
                      />

                      <button
                        className="primary-button full-button"
                        type="submit"
                        disabled={
                          isAddingContribution ||
                          isSavingGoal ||
                          activeGoal.status === 'completed'
                        }
                      >
                        {isAddingContribution
                          ? 'Recording contribution...'
                          : 'Record contribution'}
                        {!isAddingContribution && (
                          <ArrowUpRight size={17} />
                        )}
                      </button>
                    </form>
                  </>
                )}

                {savingsError && (
                  <p className="registration-error" role="alert">
                    {savingsError}
                  </p>
                )}

                {activeGoal && (
                  <button
                    className="text-link"
                    type="button"
                    onClick={startNewSavingsGoal}
                  >
                    Create another goal
                  </button>
                )}
              </article>

              <article className="panel progress-panel">
                <div className="progress-illustration">
                  <Sprout size={35} />
                </div>
                <p className="eyebrow">ONE STEP AT A TIME</p>
                <h2>
                  {activeGoal
                    ? 'Your progress'
                    : 'Every plan starts somewhere.'}
                </h2>
                <p className="section-description">
                  {activeGoal
                    ? 'Your progress reflects the contributions recorded by FoodWise.'
                    : 'Create a savings goal to start tracking your progress.'}
                </p>

                <div className="progress-track large-progress">
                  <div
                    className="progress-fill"
                    style={{ width: `${savingsProgress}%` }}
                  />
                </div>

                <div className="progress-meta">
                  <span>{Math.round(savingsProgress)}% of target</span>
                  <span>
                    {money(Math.max(0, targetValue - savedValue))} remaining
                  </span>
                </div>

                <p className="demo-disclaimer">
                  This records savings for planning purposes. No money is
                  deposited or transferred.
                </p>
              </article>
            </div>
          </section>
        )}

        {activeTab === 'Food Budget' && (
          <section className="page-layout">
            <div className="page-intro">
              <div>
                <p className="eyebrow">SPEND WITH INTENTION</p>
                <h2>Your food budget</h2>
                <p className="section-description">
                  Set a monthly amount to guide your food planning.
                </p>
              </div>
              <span className="large-page-icon">
                <Wallet size={27} />
              </span>
            </div>

            <div className="budget-layout">
              <article className="budget-highlight">
                <span className="budget-highlight-icon">
                  <CircleDollarSign size={24} />
                </span>

                <p>YOUR MONTHLY FOOD BUDGET</p>

                <h2>{money(budgetValue)}</h2>

                <span className="budget-hint">
                  {recommendedBudget
                    ? `Recommended: ${money(Number(recommendedBudget.recommended_amount))}`
                    : 'Your chosen planning amount'}
                </span>

                <button
                  className="primary-button"
                  type="button"
                  onClick={handleCreateBudget}
                  disabled={isCreatingBudget}
                >
                  {isCreatingBudget
                    ? 'Calculating...'
                    : 'Get recommended budget'}
                  {!isCreatingBudget && <ArrowUpRight size={17} />}
                </button>

                {budgetError && (
                  <p className="registration-error" role="alert">
                    {budgetError}
                  </p>
                )}

                <div className="budget-divider" />

                <div className="budget-bottom">
                  <span>
                    <CheckCircle2 size={16} /> Budget overview
                  </span>
                  <span>NGN · Naira</span>
                </div>
              </article>

              <article className="panel">
                <div className="panel-heading">
                  <div>
                    <h2>Set your budget</h2>
                    <p className="section-description">
                      You can adjust this amount whenever you need.
                    </p>
                  </div>
                </div>

                <form className="app-form" onSubmit={saveBudget}>
                  <label htmlFor="monthly-budget">
                    Monthly food budget (₦)
                  </label>
                  <input
                    id="monthly-budget"
                    type="number"
                    min="0"
                    step="500"
                    value={budget}
                    onChange={(event) => setBudget(event.target.value)}
                    placeholder="e.g. 80000"
                  />
                  <p className="field-help">
                    Consider your household needs and other monthly expenses
                    when choosing an amount.
                  </p>
                  <button
                    className="primary-button full-button"
                    type="submit"
                  >
                    Update food budget <ArrowUpRight size={17} />
                  </button>
                </form>
              </article>
            </div>

            <article className="panel budget-tip">
              <span className="tip-icon">
                <Leaf size={21} />
              </span>
              <div>
                <h3>A simple way to get started</h3>
                <p>
                  Think about the food your household needs, the meals you
                  often prepare, and how frequently you shop. You can use those
                  details to make a budget that works for you.
                </p>
              </div>
            </article>
          </section>
        )}

        {activeTab === 'AI Food Assistant' && (
          <section className="page-layout assistant-page">
            <div className="page-intro">
              <div>
                <p className="eyebrow">YOUR FOOD PLANNING PARTNER</p>
                <h2>Meet your Food Assistant</h2>
                <p className="section-description">
                  Ask for a food plan based on your income and household size.
                </p>
              </div>

              <span className="large-page-icon">
                <Sparkles size={27} />
              </span>
            </div>

            <article className="panel assistant-panel">
              <div className="assistant-welcome">
                <span className="assistant-avatar">
                  <Sparkles size={22} />
                </span>
                <div>
                  <h3>FoodWise Assistant</h3>
                  <p>
                    I can help you get a personalised food plan and
                    recommended food budget.
                  </p>
                </div>
              </div>

              <div
                className="assistant-conversation"
                aria-live="polite"
                aria-label="Food assistant conversation"
              >
                {assistantMessages.length === 0 && (
                  <div className="assistant-empty">
                    <MessageCircle size={30} />
                    <h3>What would you like help planning?</h3>
                    <p>
                      Try asking me to create a food plan for your household.
                    </p>
                    <button
                      className="assistant-suggestion"
                      type="button"
                      onClick={() =>
                        setAssistantInput('Please create a food plan for me.')
                      }
                    >
                      <Sparkles size={15} />
                      Create my food plan
                    </button>
                  </div>
                )}

                {assistantMessages.map((message, index) => (
                  <div
                    className={`assistant-message ${
                      message.role === 'user' ? 'user-message' : 'bot-message'
                    }`}
                    key={`${message.role}-${index}`}
                  >
                    <span>{message.content}</span>
                  </div>
                ))}

                {isAssistantLoading && (
                  <div className="assistant-message bot-message">
                    <span>Preparing your food plan...</span>
                  </div>
                )}
              </div>

              {assistantError && (
                <p className="registration-error" role="alert">
                  {assistantError}
                </p>
              )}

              {assistantResponse && (
                <div className="assistant-plan">
                  <p className="eyebrow">YOUR RECOMMENDED PLAN</p>
                  <h3>{assistantResponse.food_plan.recommended_package.name}</h3>

                  <div className="assistant-plan-stats">
                    <div>
                      <span>Recommended monthly budget</span>
                      <strong>
                        {money(
                          Number(
                            assistantResponse.food_plan.recommended_food_budget,
                          ),
                        )}
                      </strong>
                    </div>

                    <div>
                      <span>Estimated package cost</span>
                      <strong>
                        {money(
                          Number(
                            assistantResponse.food_plan.recommended_package
                              .estimated_cost,
                          ),
                        )}
                      </strong>
                    </div>

                    <div>
                      <span>Household size</span>
                      <strong>
                        {assistantResponse.food_plan.household_size}
                      </strong>
                    </div>

                    <div>
                      <span>Package duration</span>
                      <strong>
                        {assistantResponse.food_plan.recommended_package
                          .duration_days}{' '}
                        days
                      </strong>
                    </div>
                  </div>

                  <p className="assistant-plan-reason">
                    {assistantResponse.food_plan.reason}
                  </p>
                </div>
              )}

              <form
                className="assistant-form"
                onSubmit={handleAssistantSubmit}
              >
                <label htmlFor="assistant-message">Your message</label>

                <div className="assistant-input-row">
                  <input
                    id="assistant-message"
                    type="text"
                    value={assistantInput}
                    onChange={(event) =>
                      setAssistantInput(event.target.value)
                    }
                    placeholder="Ask for your food plan..."
                    maxLength={2000}
                    disabled={isAssistantLoading || !user}
                    required
                  />

                  <button
                    className="primary-button assistant-send"
                    type="submit"
                    disabled={
                      isAssistantLoading || !assistantInput.trim() || !user
                    }
                    aria-label="Send message"
                  >
                    <Send size={17} />
                    <span>{isAssistantLoading ? 'Sending...' : 'Send'}</span>
                  </button>
                </div>

                <p className="field-help">
                  FoodWise currently supports food-plan requests. Your
                  recommendation uses the information saved in your account.
                </p>
              </form>
            </article>
          </section>
        )}

        <footer className="app-footer">
          <span className="footer-brand">
            <Leaf size={15} /> FoodWise
          </span>
          <span>Fresh thinking for everyday food decisions.</span>
          <span className="footer-preview">FRONTEND PREVIEW</span>
        </footer>
      </main>
    </div>
  )
}

export default App
