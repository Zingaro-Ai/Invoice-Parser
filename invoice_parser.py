from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, List

load_dotenv()

raw_client = OpenAI()


class CostDetail(BaseModel):
    description: str
    type: str
    quantity: Optional[int]
    unit_price: float  # Price per unit
    total_price: float  # Total price for this item


class TotalCost(BaseModel):
    bill_amount: float


class ContractDetails(BaseModel):
    detailed_breakdown_of_costs: List[CostDetail] = Field(
        description="detailed breakdown of costs",
    )

    total_bill_amount: float = Field(description="""
    The total bill amount for all services and materials listed on the invoice, before any payments or credits are applied.
    - **Includes**: The aggregate of all line-item costs, taxes, fees, and any other charges related to the contract.
    - **Purpose**: Provides a clear, complete view of the full cost of services rendered, as documented in the invoice.
    - **Precision**: Stored with exact decimal precision to maintain accuracy in financial records and calculations.
    """
                                     )

    scope_of_work: str = Field(
    description=""" 
    - The scope of work refers to the specific tasks, responsibilities, and deliverables that a contractor is expected to perform as outlined in the contract or invoice.
    - It should clearly describe the nature and extent of the services provided, including any technical details, timelines, and requirements.
    - To get the perfect scope of work:
      1. Extract any explicitly stated tasks or services from the contractor's invoice or contract.
      2. If the scope is not clearly mentioned, attempt to infer it from related project details (e.g., service categories, specific tasks, or frequency).
      3. Ensure that all relevant work is captured and avoid vague or overly broad statements.
      4. If no clear scope is identified from the available information, return an empty string.
    """
    )
    # payment_terms: str = Field(
    #     description="details on how and when payments are due. if not in the invoice return empty string"
    # )

    payment_schedule: str = Field(
    description="""
        The agreed-upon structure for how and when payments will be made toward the total bill amount.
        - **Includes**: Specific terms regarding payment intervals (e.g., upfront, periodic installments, or milestone-based payments) as outlined in the contract.
        - **Purpose**: Provides clarity on the timing and amounts of payments required, supporting both parties in managing expectations and cash flow.
        - **Precision**: Details should be stored accurately to avoid discrepancies, ensuring consistency with the contract terms.
    """
    )


    accepted_payment_methods: str = Field(
    description="""
    The forms of payment that are accepted to settle the total bill amount.
    - **Includes**: A list of accepted payment types, such as bank transfers, checks, credit cards, digital wallets, or other methods specified by the service provider.
    - **Purpose**: Provides clarity on how payments can be made, ensuring that both the payer and the service provider are aligned on available options.
    - **Precision**: Stored in a clear and specific format to avoid misunderstandings, supporting seamless payment processing.
    """
    )

    penalties_for_late_payment: str = Field(
    description="""
    Additional charges or fees that may be applied if payment is not made by the specified due date.
    - **Includes**: Details on the rate or amount of late fees, grace periods (if any), and the conditions under which penalties are applied.
    - **Purpose**: Provides transparency around the consequences of late payments, encouraging timely settlement and outlining potential financial impacts.
    - **Precision**: Clearly defined to ensure enforceability and understanding by all parties, aligning with the terms agreed upon in the contract.
    """
    )

    # payment_terms: str = Field(
    #     description="details on how and when payments are due. if not in the invoice return empty string"
    # )

    invoice_date: str = Field(
        description="""
    The date the invoice was issued, marking the official record for the start of payment terms and transaction timeline.
    - **Importance**: Essential for tracking when the billing cycle begins and for determining payment deadlines.
    - **Format**: Should be in a standard date format (e.g., YYYY-MM-DD) to maintain consistency in financial records.
    - **Behavior if Missing**: If no invoice date is found on the invoice, this field will return an empty string.
    """
    )

    due_date: Optional[str] = Field(description="""
    The final date by which the payment is expected to be made for this invoice, marking the payment deadline.
    - This date is critical for maintaining payment schedules and determining any overdue payments or penalties.
    - Ensure the date is accurately captured in a consistent format (e.g., YYYY-MM-DD) to support clear financial tracking.
    - If the due date is not explicitly mentioned in the invoice, return an empty string.
    """
                                    )

    project_milestones_or_phases: Optional[str] = Field(
        description="""
    Specific stages or milestones of the project covered by this invoice, detailing the work progress or phases completed.
    - This field is important for tracking project progress and understanding the context of billed work relative to the overall project.
    - It may include descriptions of completed phases, percentage completion, or any key accomplishments.
    - If no milestones or phases are specified in the invoice, return an empty string.
    """
    )

    applicable_taxes: float = Field(
        description="""
    The total amount of taxes applied to the invoice, calculated as a percentage or fixed rate based on the relevant tax regulations.
    - This field represents the tax cost associated with the billed services or items, ensuring clarity in the total billing amount.
    - If no taxes are applicable or mentioned in the invoice, this field should return `None`.
    """
    )

    change_orders: Optional[str] = Field(
        description="""
    Details of any changes or modifications to the original contract, including adjustments in scope, timeline, or cost.
    - This field reflects agreed-upon amendments to the initial contract terms, providing a record of alterations made.
    - If no change orders are present or explicitly mentioned in the invoice, this field should return an empty string.
    """)

    contractor_contact_info: Optional[str] = Field(description="""
    The contact information for the contractor, including details such as name, address, phone number, and email, if provided.
    - This field allows for direct communication with the contractor and serves as a point of reference for any inquiries or clarifications.
    - If contractor contact information is not explicitly stated in the invoice, this field should return an empty string.
    """)

    contractor_license_number: Optional[str] = Field(
        description="""
    The license number of the contractor, providing a reference to verify the contractor’s credentials and compliance.
    - This field is important for legal and regulatory purposes, especially if the project requires licensed professionals.
    - If the license number is not specified on the invoice, this field should return an empty string.
    """)

    contractor_insurance: Optional[str] = Field(
        description="""
    The contractor’s insurance information, typically including details about coverage for liability or workers' compensation.
    - This field ensures transparency regarding any insurance coverage in place, which can protect both the contractor and client.
    - If no insurance information is mentioned in the invoice, this field should return an empty string.
    """)

    warranties_or_guarantees: Optional[str] = Field(
        description="""
    Any warranties or guarantees provided by the contractor for the work or materials used in the project.
    - This field highlights any commitments made to quality or workmanship, outlining what aspects are covered and the duration of coverage.
    - If warranties or guarantees are not explicitly included in the invoice, this field should return an empty string.
    """)

    signatures: str = Field(
        description=""" contractor's hand written signature. if you dont find return empty string"""
    )

    permits_and_inspection_fees: Optional[float] = Field(description="""
    The fees associated with any necessary permits or inspections required for the project.
    - This may include costs for obtaining building permits, safety inspections, or other regulatory fees.
    - If no permit or inspection fees are mentioned in the invoice, this field should return None.
    """
                                                         )

    retainage: Optional[float] = Field(description="""
    The amount of money that is withheld from the total payment until the completion of the project.
    - Retainage is often used as a security measure to ensure that the contractor fulfills their obligations.
    - If retainage details are not provided in the invoice, this field should return None.
    """
                                       )

    discounts_or_promotions: Optional[float] = Field(description="""
    Any discounts or promotional offers applied to the total bill amount, which may reduce the final payment due.
    - This field captures information about any agreed-upon price reductions, including seasonal discounts or negotiated rates.
    - If no discounts or promotions are mentioned in the invoice, this field should return None.
    """
                                                     )


class InvoiceOutput(BaseModel):
    error: List[str] = Field(
        description="list of error messages for missing mandatory fields in invoice"
    )
    warning: List[str] = Field(
        description="list of warning messages for missing mandatory fields in invoice"
    )




def extract_invoice_elements(encoded_image):
    completion = raw_client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
Role: You are an invoice extractor, responsible for identifying and extracting essential elements from an invoice provided by a home improvement contractor. Your task is to ensure each field is captured accurately:

detailed_breakdown_of_costs: Extract an itemized list of all costs involved in the project.

scope_of_work: Capture a clear description of the tasks and services covered under this contract.

payment_schedule: The agreed-upon schedule specifying when and how payments toward the total bill amount will be made

accepted_payment_methods: The types of payments accepted to settle the total bill amount, such as bank transfers, checks, or credit cards.

penalties_for_late_payment: Charges or fees applied if payment is not made by the due date, including details on rates, grace periods, and conditions.

invoice_date: Extract the date when the invoice was issued.

due_date: Capture the payment deadline specified on the invoice.

project_milestones_or_phases: Identify any major stages or phases outlined for tracking project progress.

applicable_taxes: Extract any taxes applied to the project costs.

change_orders: Capture documentation of any agreed-upon changes that affect cost or scope.

contractor_contact_info: Extract the contractor's contact details.

contractor_license_number: Identify the contractor’s licensing information for verification.

contractor_insurance: Capture proof of insurance to cover potential liabilities.

warranties_or_guarantees: Extract any warranties or guarantees on workmanship or materials.

permits_and_inspection_fees: Identify fees related to permits or inspections, if applicable.

retainage: Capture any amount withheld until project completion, if applicable.

discounts_or_promotions: Extract details of any agreed discounts or special promotions applied.

signatures: Identify signatures indicating acceptance of the invoice.

Your goal is to ensure each of these fields is accurately extracted to validate the completeness of the invoice and facilitate further processing.                     
""",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        },
                    },
                ],
            }
        ],
        response_format=ContractDetails
    )
    return completion.choices[0].message.parsed








if __name__ == "__main__":
    image_path ="/home/kuro/Pictures/Screenshots/Screenshot from 2024-12-09 19-55-23.png"
    results =extract_invoice_elements(image_path)
    print(results.dict())