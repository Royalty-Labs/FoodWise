# FoodWise Testing Guide

This guide describes how to run checks and verify the FoodWise frontend, backend API, and assistant integration during development.

## 1. Backend Tests

Open PowerShell at the repository root and run:

```powershell
cd backend
```

Activate the virtual environment if it is not already active:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install pytest if it is not available:

```powershell
python -m pip install pytest
```

Run the test suite:

```powershell
python -m pytest
```

Review the output for failed tests, errors, or skipped tests. Record failures and investigate them before treating a change as verified.

## 2. Frontend Checks

Open a separate PowerShell terminal and navigate to the frontend directory:

```powershell
cd frontend
```

Install dependencies if necessary:

```powershell
npm install
```

Run the production build:

```powershell
npm run build
```

Run the configured lint checks:

```powershell
npm run lint
```

A successful build confirms that the production bundle can be generated. It does not, by itself, confirm that every screen or API interaction works correctly.

## 3. API Verification

Start the backend locally:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Open the interactive API documentation:

`http://127.0.0.1:8000/docs`

Use the documented endpoints to verify request validation, response structures, expected status codes, and error handling.

Test only endpoints and request formats that are actually defined by the current application.

## 4. Database Verification

When testing features that depend on PostgreSQL:

- Confirm that the configured database is reachable.
- Confirm that required migrations have been applied.
- Test expected behaviour when records exist and when they do not.
- Check validation for invalid or incomplete input.
- Avoid using production data for destructive tests.

Apply migrations in the appropriate development environment when required:

```powershell
alembic upgrade head
```

## 5. FoodWise Feature Checks

Use the following checklist when validating application changes.

- [ ] Budget calculations use the expected income and household information.
- [ ] Food-plan recommendations return valid results.
- [ ] Savings operations handle valid and invalid inputs appropriately.
- [ ] Food packages display the expected information.
- [ ] Recommendations handle missing or incomplete data safely.
- [ ] The frontend displays API errors clearly.
- [ ] The assistant handles supported requests and unsuitable input appropriately.

The checklist is a testing plan, not a claim that all checks have already passed.

## 6. N-ATLaS Assistant Checks

If the local N-ATLaS server is enabled, verify the model endpoint independently before testing the complete application flow.

Check:

- [ ] The model server starts and accepts requests.
- [ ] The chat-completions endpoint returns a valid response.
- [ ] The FoodWise backend can reach the configured model server.
- [ ] The frontend receives and displays the assistant response.
- [ ] Food-plan requests are routed and handled as expected.
- [ ] Timeouts and unavailable-model errors are handled appropriately.
- [ ] Response latency is measured.
- [ ] English, Yoruba, Igbo, and Hausa are evaluated independently.
- [ ] Speech functionality is tested separately if implemented.

A successful direct model request does not guarantee that the complete FoodWise assistant workflow works.

## 7. Live Deployment Checks

The deployed application can be checked at:

- Frontend: https://foodwise-frontend.onrender.com
- Backend: https://foodwise-jum9.onrender.com
- API documentation: https://foodwise-jum9.onrender.com/docs

Verify the live environment separately from local development. A successful local test does not prove that the deployed environment has the same configuration or dependencies.

## 8. Reporting Test Results

When documenting test results, include:

- The command or action performed.
- The environment tested: local or deployed.
- Whether the test passed, failed, or was skipped.
- Relevant error messages, excluding secrets.
- Any unresolved issues.

Do not claim that a test passed unless it was actually run and its result was checked.

## Related Documentation

- [Development Setup](development-setup.md)
- [N-ATLaS Integration](n-atlas-integration.md)
- [Backend README](../backend/README.md)
- [Frontend README](../frontend/README.md)