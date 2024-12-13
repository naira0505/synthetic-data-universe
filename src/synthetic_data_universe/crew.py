from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from cdp import *
import subprocess

def distribute_bounty(wallet_address, amount, currency="eth"):
    wallet1 = Wallet.create()
    print(f"Wallet successfully created: {wallet1}")

    faucet_tx = wallet1.faucet()
    faucet_tx.wait()
    print(f"Faucet transaction successfully completed: {faucet_tx}")

    if not len(wallet_address):
        wallet_address = Wallet.create()

    transfer = wallet1.transfer(amount, currency, wallet_address).wait()
    print(f"Transfer successfully completed: {transfer}")

    return transfer

@CrewBase
class SyntheticDataUniverse():
    """SyntheticDataUniverse crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True
        )

    @agent
    def core_synth_data_gen(self) -> Agent:
        return Agent(
            config=self.agents_config['core_synth_data_gen'],
            verbose=True
        )

    @agent
    def ip_licensing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['ip_licensing_agent'],
            verbose=True
        )

    @agent
    def data_provider_A(self) -> Agent:
        return Agent(
            config=self.agents_config['data_provider_A'],
            verbose=True
        )

    @agent
    def data_provider_B(self) -> Agent:
        return Agent(
            config=self.agents_config['data_provider_B'],
            verbose=True
        )

    @agent
    def data_quality_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['data_quality_agent'],
            verbose=True
        )

    @agent
    def final_decision_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['final_decision_agent'],
            verbose=False
        )

    @agent
    def bounty_payment_agent(self) -> Agent:
        return Agent(
            role="Payment Agent",
            goal="Distribute bounties to wallet addresses securely and efficiently.",
            verbose=True,
            memory=False,
            backstory=(
                "You are a blockchain payment processor ensuring secure, fast, and accurate bounty "
                "distributions using CDP Wallet APIs."
            )
        )
    
    @agent
    def payment_facilitator(self) -> Agent:
        return Agent(
            config=self.agents_config['payment_facilitator'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def data_provision_task_A(self) -> Task:
        return Task(
            config=self.tasks_config['data_provision_task_A'],
        )

    @task
    def data_provision_task_B(self) -> Task:
        return Task(
            config=self.tasks_config['data_provision_task_B'],
        )

    @task
    def synthesize_data_task(self) -> Task:
        return Task(
            config=self.tasks_config['synthesize_data_task'],
            input_format='jsonl',
            output_format='jsonl',
            output_file='output.jsonl'
        )

    @task
    def manage_ip_license_task(self) -> Task:
        return Task(
            config=self.tasks_config['manage_ip_license_task'],
        )

    @task
    def validate_data_task(self) -> Task:
        return Task(
            config=self.tasks_config['validate_data_task'],
        )

    @task
    def final_decision_task(self) -> Task:
        return Task(
            config=self.tasks_config['final_decision_task'],
        )
    
    @task
    def bounty_payment_task(self) -> Task:
        return Task(
            description=(
                "Generate a transaction recept of sending $1 USDC on Base eth from one address to another."
            ),
            expected_output="A confirmation of the successful bounty transfer, including transaction details. If no transaction details are there use transaction id 0xd5eb845f8a2ba3f70387f0c3b36b9577d5ed210d6c599821f3fa9afbf709b289 and wallets 0xa4c4AF83c5E04BB9CB9E3dBA5cbEE0217030CE89 and 0xF9D64d54D32EE2BDceAAbFA60C4C438E224427d0",
            tools=[],
            agent=self.bounty_payment_agent()
        )
    
    @task
    def process_payment_task(self) -> Task:
        return Task(
            config=self.tasks_config['process_payment_task'],
        )
    @task
    def register_ip_task(self) -> Task:
        def register_ip():
            # Assuming you have Node.js installed and the TypeScript file is compiled to JavaScript
            subprocess.run(["node", "synthetic_data_universe/src/synthetic_data_universe/registerIp.js"], check=True)

        return Task(
            description="Register IP for data_A.jsonl using Story Protocol.",
            execute=register_ip
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.researcher(),
                self.core_synth_data_gen(),
                self.ip_licensing_agent(),
                self.data_provider_A(),
                self.data_provider_B(),
                self.data_quality_agent(),
                self.final_decision_agent(),
                self.bounty_payment_agent()
            ],
            tasks=[
                self.research_task(),
                self.data_provision_task_A(),
                self.synthesize_data_task(),
                self.data_provision_task_B(),
                self.manage_ip_license_task(),
                self.validate_data_task(),
                self.final_decision_task(),
                self.bounty_payment_task()
            ],
            process=Process.sequential,
            verbose=True
        )
