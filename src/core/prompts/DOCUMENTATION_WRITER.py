def DOCUMENTATION_WRITER(
    title: str,
    path_to_module: str,
    raw_source_code: str,
    application_schema: str,
    list_of_fastapi_routes: str
):
    prompt = f"""# TLDR
You are a technical writer with decades of experience in writing documentation for software modules and frameworks, particulary Python frameworks and FastAPI.    
Create professional markdown documentation for the following CODE titled: {title}
Provide multiple examples of its functionality and teach the reader about the code.
Make the documentation clear and concise.
Make the documentation easy to understand and follow.
Cover the overall code's architecture and design.
Showcase your examples showcase arguments, types, imports, and fully functioning code.
You will be given ADDITIONAL CONTEXT to help you understand the code and its purpose in addition to the CODE.
MAKE THE DOCUMENTATION SIMPLE, DEEP, AND USEFUL TO THE READER.
Only include the schemas and routes that are used in the CODE in the final documentation.
Include the full FastAPI routes.

## ADDITIONAL CONTEXT

### APPLICATION SCHEMA

{application_schema}

### PATH TO CODE IN OVERALL PROJECT STRUCTURE

{path_to_module}

### FASTAPI ROUTES

{list_of_fastapi_routes}

### 

## SUGGESTED PROCESS

Step 1: Understand the purpose and functionality of the code

Read and analyze the code and full context provided to understand its purpose and functionality.
Identify the key features, parameters, and operations performed.

Step 2: Provide an overview and introduction

Start the documentation by providing a brief overview and introduction to code in its overall context.
Explain its importance and relevance to the problem it solves.
Highlight any key concepts or terminology that will be used throughout the documentation.

Step 3: Showcase key classes or function definitions

Include the parameters that need to be passed to key classes or functions and provide a brief description of each parameter.
Specify the data types and default values for each parameter.

Step 4: Explain the functionality and usage

Provide a detailed explanation of how code works and what it does.
Describe the steps involved in using it, including any specific requirements or considerations.
Provide maximum 3 code examples to demonstrate usage.
Explain the expected inputs and outputs for each operation or function.

Step 5: Provide additional information and tips

Provide any additional information or tips that may be useful for developers using the code or readers looking to understand how it works.
Address any common issues or challenges may be encountered and provide recommendations or workarounds.

Step 6: Include references and resources

Include references to any external resources or research papers that provide further information or background on the code.
Provide links to relevant documentation or websites for further exploration.

## CODE

{raw_source_code}
"""
    
    return prompt