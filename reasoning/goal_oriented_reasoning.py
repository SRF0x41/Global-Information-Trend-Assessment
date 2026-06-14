import requests
import logging
from typing import List, Dict


class GoalReasoner:
    def __init__(
        self,
        model_name: str,
        api_url: str = "http://127.0.0.1:1234/v1/chat/completions",
    ):
        self.model_name = model_name
        self.api_url = api_url
        self.logger = logging.getLogger(__name__)

    def _get_lmstudio_response(self, prompt: str) -> str:
        """Send a prompt to LM Studio and return the response text."""

        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "stream": False,
        }

        response = requests.post(self.api_url, json=payload, timeout=120)

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]

    def _decompose_goal(self, goal: str) -> List[Dict]:
        """Break a goal into steps."""

        prompt = f"""
            Break down the following goal into numbered actionable steps.

            Goal:
            {goal}

            Return only numbered steps.

            Example:
            1. First step
            2. Second step
            3. Third step
            """

        try:
            content = self._get_lmstudio_response(prompt)

            steps = []

            for line in content.splitlines():
                line = line.strip()

                if not line:
                    continue

                if line[0].isdigit():
                    parts = line.split(".", 1)

                    if len(parts) > 1:
                        steps.append(
                            {
                                "goal": parts[1].strip(),
                                "completed": False,
                                "result": None,
                            }
                        )

            return steps

        except Exception as e:
            self.logger.error(f"Goal decomposition failed: {e}")
            return []

    def _execute_step(self, step: Dict) -> bool:
        """Execute a step using the model."""

        prompt = f"""
            Complete the following task:

            {step['goal']}

            Provide a concise answer.
            """

        try:
            result = self._get_lmstudio_response(prompt)

            if result.strip():
                step["result"] = result
                step["completed"] = True

                self.logger.info(f"Completed step: {step['goal']}")

                return True

            return False

        except Exception as e:
            self.logger.error(f"Step execution failed: {e}")
            return False

    def reason_towards_goal(self, goal: str) -> bool:
        """Main reasoning loop."""

        steps = self._decompose_goal(goal)

        if not steps:
            self.logger.error("No valid steps generated for the goal")
            return False

        print("\nGenerated Steps:")
        print("-" * 50)

        for i, step in enumerate(steps, start=1):
            print(f"{i}. {step['goal']}")

        print("-" * 50)

        while not all(step["completed"] for step in steps):
            current_step = next((step for step in steps if not step["completed"]), None)

            if current_step is None:
                break

            print(f"\nExecuting: {current_step['goal']}")

            success = self._execute_step(current_step)

            if not success:
                self.logger.error(
                    f"Failed to complete step: " f"{current_step['goal']}"
                )
                return False

            print("\nResult:")
            print(current_step["result"])

        print("\nExecution Summary")
        print("-" * 50)

        for i, step in enumerate(steps, start=1):
            print(f"\nStep {i}: {step['goal']}")
            print(f"Result: {step['result']}")

        self.logger.info("Goal achieved")

        return True


# if __name__ == "__main__":

#     logging.basicConfig(
#         level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
#     )

#     # Replace with the exact model ID from:
#     # curl http://127.0.0.1:1234/v1/models
#     MODEL_NAME = "qwen/qwen3-14b"

#     reasoner = GoalReasoner(model_name=MODEL_NAME)

#     goal = "Solve the equation 2x + 3 = 7"

#     print("=" * 60)
#     print("Goal Reasoner")
#     print("=" * 60)
#     print(f"Goal: {goal}")

#     try:
#         success = reasoner.reason_towards_goal(goal)

#         if success:
#             print("\nGoal successfully achieved.")
#         else:
#             print("\nFailed to achieve goal.")

#     except Exception as e:
#         print(f"\nFatal error: {e}")
