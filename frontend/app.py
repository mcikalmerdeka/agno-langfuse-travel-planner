"""Gradio interface for the Travel Planning Workflow."""
import gradio as gr
import asyncio


def create_gradio_interface(plan_trip_func):
    """
    Create a modern Gradio interface for the travel planning workflow.
    
    Args:
        plan_trip_func: The async function that runs the travel planning workflow
        
    Returns:
        gr.Blocks: Configured Gradio interface
    """
    
    # Custom CSS for dark theme UI
    custom_css = """
    .gradio-container {
        max-width: 1200px !important;
        margin: auto !important;
        background: #1a1a1a !important;
    }
    
    .header-box {
        background: #000000;
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #ffffff;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
        color: #ffffff;
    }
    
    .workflow-info {
        background: #2d2d2d;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #ffffff;
        margin: 1rem 0;
        color: #ffffff;
    }
    
    .example-card {
        background: #2d2d2d;
        border: 1px solid #444444;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #ffffff;
    }
    
    .example-card:hover {
        border-color: #ffffff;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.15);
    }
    
    .status-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .status-running {
        background: #3d3d00;
        border-left: 4px solid #ffc107;
        color: #ffffff;
    }
    
    .status-complete {
        background: #003d00;
        border-left: 4px solid #28a745;
        color: #ffffff;
    }
    
    .status-error {
        background: #3d0000;
        border-left: 4px solid #dc3545;
        color: #ffffff;
    }
    
    #output-box {
        background: #2d2d2d;
        border: 1px solid #444444;
        border-radius: 8px;
        padding: 1.5rem;
        min-height: 400px;
        color: #ffffff;
    }
    
    .footer-info {
        text-align: center;
        padding: 1rem;
        color: #cccccc;
        font-size: 0.9rem;
        margin-top: 2rem;
    }
    
    /* Dark theme for all Gradio components */
    .dark, .dark * {
        color: #ffffff !important;
    }
    
    /* Textbox styling */
    textarea, input[type="text"] {
        background: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
    }
    
    /* Button styling */
    .primary {
        background: #000000 !important;
        border: 2px solid #ffffff !important;
        color: #ffffff !important;
    }
    
    .secondary {
        background: #2d2d2d !important;
        border: 1px solid #ffffff !important;
        color: #ffffff !important;
    }
    
    /* Markdown output styling */
    .prose {
        color: #ffffff !important;
    }
    
    .prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6 {
        color: #ffffff !important;
    }
    
    .prose p, .prose li, .prose span {
        color: #ffffff !important;
    }
    
    .prose code {
        background: #1a1a1a !important;
        color: #ffffff !important;
    }
    
    .prose pre {
        background: #1a1a1a !important;
        border: 1px solid #444444 !important;
    }
    
    /* Accordion styling */
    .accordion {
        background: #2d2d2d !important;
        border: 1px solid #444444 !important;
    }
    
    /* Label styling */
    label {
        color: #ffffff !important;
    }
    """
    
    # Store the latest travel plan for export
    latest_travel_plan = {"content": ""}
    
    # Wrapper function to handle async execution
    def run_travel_planner(query: str):
        """
        Wrapper function to run the async travel planning workflow.
        
        Args:
            query: User's travel planning query
            
        Returns:
            tuple: (status_message, result_markdown, export_btn_visible, pdf_file_visible)
        """
        if not query or not query.strip():
            return (
                "⚠️ Please enter a valid travel planning query.",
                "## No Query Provided\n\nPlease enter your travel planning requirements in the text box above.",
                gr.update(visible=False),  # Hide copy button
                ""  # Clear markdown storage
            )
        
        try:
            # Run the async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            result = loop.run_until_complete(plan_trip_func(query))
            loop.close()
            
            if result and result.content:
                status_msg = "✅ **Travel Plan Generated Successfully!**"
                
                # Format the result
                result_markdown = f"""

{result.content}

---

### 📊 Workflow Information
- **Workflow:** Travel Planning with Manager Approval
- **Research Agents:** Destination, Hotels, Activities (ran in parallel)
- **Planning Agent:** Itinerary Planner (Team Lead)
- **Review Agent:** Critique Agent (Manager)
- **Status:** ✅ Approved and Complete

---

*Generated by Travel Planning AI Workflow*
"""
                # Store the latest plan for export
                latest_travel_plan["content"] = result_markdown
                
                return (
                    status_msg, 
                    result_markdown,
                    gr.update(visible=True),   # Show copy button
                    result_markdown  # Store in hidden textbox for copying
                )
            else:
                return (
                    "⚠️ **Workflow completed but no result was generated.**",
                    "## No Result\n\nThe workflow completed but did not return a travel plan. Please try again.",
                    gr.update(visible=False),  # Hide copy button
                    ""  # Clear markdown storage
                )
                
        except Exception as e:
            error_msg = f"❌ **Error occurred during planning:** {str(e)}"
            error_detail = f"""## ❌ Error Occurred

**Error Message:**
```
{str(e)}
```

**What to do:**
1. Check your API keys in the `.env` file
2. Ensure all required services (Langfuse, OpenAI, Tavily) are accessible
3. Try a simpler query
4. Check the terminal for detailed error logs

**Need Help?**
Review the README.md for setup instructions.
"""
            return (
                error_msg, 
                error_detail,
                gr.update(visible=False),  # Hide copy button
                ""  # Clear markdown storage
            )
    
    # Create the Gradio interface with dark theme
    with gr.Blocks(css=custom_css, theme=gr.themes.Base(primary_hue="slate", secondary_hue="slate").set(
        body_background_fill="#1a1a1a",
        body_background_fill_dark="#1a1a1a",
        block_background_fill="#2d2d2d",
        block_background_fill_dark="#2d2d2d",
        input_background_fill="#2d2d2d",
        input_background_fill_dark="#2d2d2d",
        block_label_text_color="#ffffff",
        block_title_text_color="#ffffff",
        body_text_color="#ffffff",
        body_text_color_subdued="#cccccc",
    ), title="🌏 Travel Planning AI") as interface:
        
        # Header
        gr.HTML("""
        <div class="header-box">
            <div class="header-title">🌏 Travel Planning AI</div>
            <div class="header-subtitle">Powered by Agno Workflow + Langfuse Tracing</div>
        </div>
        """)
        
        # Workflow info
        with gr.Accordion("ℹ️ How It Works", open=False):
            gr.Markdown("""
            ### 🔄 Workflow Architecture
            
            This AI-powered travel planner uses a multi-agent workflow:
            
            1. **🔍 Research Team (Parallel)** - Three agents work simultaneously:
               - 🏛️ Destination Researcher - Finds attractions and cultural insights
               - 🏨 Hotel Finder - Searches for accommodations matching your budget
               - 🎭 Activities Researcher - Discovers experiences and local cuisine
            
            2. **📋 Team Lead (Itinerary Planner)** - Creates comprehensive travel plan
            
            3. **✅ Manager (Critique Agent)** - Reviews and approves the plan
            
            4. **🔄 Revision Loop** - If needed, the planner revises based on feedback
            
            5. **📋 Final Delivery** - You receive the manager-approved travel plan!
            
            **Observability:** All steps are traced with Langfuse for full transparency.
            """)
        
        # Main interface
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📝 Your Travel Query")
                
                query_input = gr.Textbox(
                    label="Describe your ideal trip",
                    placeholder="Example: Plan a 5-day trip to Kyoto, Japan for a solo traveler interested in temples, traditional culture, and local food. Budget is mid-range.",
                    lines=5,
                    max_lines=10
                )
                
                with gr.Row():
                    submit_btn = gr.Button("🚀 Generate Travel Plan", variant="primary", size="lg")
                    clear_btn = gr.Button("🗑️ Clear", variant="secondary")
                
                # Example queries
                gr.Markdown("### 💡 Example Queries")
                
                examples = [
                    "Plan a 7-day romantic trip to Paris, France for a couple. Include museums, fine dining, and scenic walks. Luxury budget.",
                    "Plan a 5-day adventure trip to Bali, Indonesia for a solo traveler. Focus on surfing, hiking, and local culture. Budget-friendly.",
                    "Plan a 4-day family trip to Tokyo, Japan with 2 kids (ages 8 and 10). Include kid-friendly activities, theme parks, and safe accommodations. Mid-range budget.",
                    "Plan a 6-day cultural immersion trip to Istanbul, Turkey. Interested in history, architecture, and authentic Turkish cuisine. Mid-range budget.",
                    "Plan a 10-day backpacking trip through Thailand (Bangkok, Chiang Mai, Islands). Focus on street food, temples, and beaches. Budget-conscious."
                ]
                
                gr.Examples(
                    examples=examples,
                    inputs=query_input,
                    label=None
                )
        
        # Status and output section
        with gr.Column(scale=1):
            gr.Markdown("### 📊 Status & Results")
            
            status_output = gr.Markdown(
                value="💤 **Ready to plan your trip!** Enter your query and click 'Generate Travel Plan'.",
                elem_id="status-box"
            )
            
            result_output = gr.Markdown(
                value="",
                elem_id="output-box"
            )
            
            # Copy button and hidden textbox for clipboard
            copy_btn = gr.Button("📋 Copy to Clipboard", variant="secondary", size="sm", visible=False)
            markdown_storage = gr.Textbox(visible=False, elem_id="markdown-storage")
        
        # Footer
        gr.HTML("""
        <div class="footer-info">
            <p>📊 All workflows are traced with Langfuse | ⚡ Powered by Agno + OpenAI</p>
        </div>
        """)
        
        # Event handlers
        submit_btn.click(
            fn=run_travel_planner,
            inputs=[query_input],
            outputs=[status_output, result_output, copy_btn, markdown_storage],
            api_name="generate_travel_plan"
        )
        
        clear_btn.click(
            fn=lambda: (
                "",
                "💤 **Ready to plan your trip!** Enter your query and click 'Generate Travel Plan'.",
                "",
                gr.update(visible=False),
                ""
            ),
            inputs=None,
            outputs=[query_input, status_output, result_output, copy_btn, markdown_storage]
        )
        
        # Copy button handler - uses JavaScript to copy from hidden textbox
        copy_btn.click(
            fn=None,
            inputs=[markdown_storage],
            outputs=None,
            js="(text) => {navigator.clipboard.writeText(text); return text;}"
        )
    
    return interface
