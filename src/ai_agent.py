"""
Yucatan PropTech AI Agent

Core AI agent powered by Claude API for real estate investment guidance
in the Yucatan Peninsula. Provides fideicomiso guidance, property analysis,
and market intelligence.
"""

import os
from anthropic import Anthropic

SYSTEM_PROMPT = """You are an expert real estate investment advisor specializing in
the Yucatan Peninsula, Mexico. You have deep knowledge of:

1. Mexican real estate law, especially fideicomiso (bank trust) requirements
2. The Yucatan property market (Merida, Valladolid, Tulum, Playa del Carmen, etc.)
3. Investment analysis and ROI projections for Mexican properties
4. The process foreign nationals must follow to purchase property in restricted zones
5. Local market trends, neighborhood analysis, and property valuation

You communicate in both English and Spanish, adapting to the user's preferred language.
You provide accurate, actionable advice while always recommending professional legal
consultation for final decisions.

IMPORTANT: Always clarify that you provide guidance and analysis, not legal advice.
Recommend consulting with a Mexican real estate attorney (notario publico) for
all legal matters."""


class YucatanPropertyAgent:
    """AI-powered real estate agent for Yucatan Peninsula investments."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY environment "
                "variable or pass api_key parameter."
            )
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"
        self.conversation_history = []

    def _send_message(self, user_message: str, system: str = None) -> str:
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system or SYSTEM_PROMPT,
            messages=self.conversation_history
        )
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        return assistant_message

    def guide_fideicomiso(self, nationality: str, property_type: str,
                          location: str, budget_usd: float) -> str:
        prompt = f"""A {nationality} national wants to purchase a {property_type}
property in {location}, Yucatan with a budget of ${budget_usd:,.0f} USD.

Please provide:
1. Whether a fideicomiso is required for this location and buyer
2. Step-by-step process to establish the fideicomiso
3. Estimated costs and timeline
4. Required documents
5. Recommended banks that offer fideicomiso services in the area
6. Key risks and how to mitigate them
7. Tax implications for the buyer"""
        return self._send_message(prompt)

    def analyze_property(self, address: str, price_mxn: float,
                         property_type: str, size_m2: float = None,
                         additional_details: str = None) -> str:
        prompt = f"""Analyze this Yucatan property for investment potential:

- Address: {address}
- Listed Price: ${price_mxn:,.0f} MXN
- Type: {property_type}
{f'- Size: {size_m2} m2' if size_m2 else ''}
{f'- Details: {additional_details}' if additional_details else ''}

Please provide:
1. Price assessment (fair market value estimate)
2. Investment score (1-10) with justification
3. Rental income potential (short-term and long-term)
4. Neighborhood analysis
5. Growth potential and appreciation forecast
6. Risk factors specific to this property/area
7. Comparable properties analysis"""
        return self._send_message(prompt)

    def market_query(self, question: str) -> str:
        return self._send_message(question)

    def reset_conversation(self):
        self.conversation_history = []


def main():
    print("=" * 60)
    print("Yucatan PropTech AI - Property Investment Assistant")
    print("=" * 60)
    print("\nPowered by Claude AI | Type 'quit' to exit\n")

    try:
        agent = YucatanPropertyAgent()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set your ANTHROPIC_API_KEY environment variable.")
        return

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("\nHasta luego!")
            break
        if not user_input:
            continue
        print("\nAnalyzing...")
        response = agent.market_query(user_input)
        print(f"\nAgent: {response}")


if __name__ == "__main__":
    main()
