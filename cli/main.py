"""
CLI orchestrator for CODE_Sherpa pipeline.

Pipeline definition (execution order):
    1. analyze   → Static analysis (always runs)
    2. enrich    → Semantic enrichment (optional, controlled by decision logic)
    3. tour      → Guided tour generation
    4. flowchart → Flowchart generation

Control flow:
    - CLI explicitly decides: when enrichment runs, which file downstream consumes
    - Each step consumes a clearly chosen input file
    - Pipeline behavior is declared, not inferred
"""
import sys
import os
import json
import subprocess
from typing import Tuple

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from analyzer.analyzer import build_unified_model
from enrich.enrich import enrich_file


# ============================================================
# Decision Logic (explicit control points)
# ============================================================

def should_enrich() -> Tuple[bool, bool]:
    """
    Explicit decision: Should enrichment run?
    
    Returns:
        (should_run: bool, use_llm: bool)
        - should_run: True if enrichment should be attempted
        - use_llm: True if LLM should be used (requires API key)
    
    Decision logic:
        - Enrichment always attempted (graceful fallback if it fails)
        - LLM only used if GROQ_API_KEY is set
    """
    use_llm = bool(os.getenv("GROQ_API_KEY"))
    should_run = True  # Always attempt (may fallback on failure)
    return should_run, use_llm


def select_input_file(analysis_file: str, enriched_file: str) -> str:
    """
    Explicit decision: Which file should downstream steps consume?
    
    Decision logic:
        - Prefer enriched file if it exists and is valid
        - Fallback to analysis file otherwise
        
    This is the single source of truth for file selection.
    """
    if os.path.exists(enriched_file):
        # Verify it's valid JSON before using
        try:
            with open(enriched_file, "r", encoding="utf-8") as f:
                json.load(f)
            return enriched_file
        except (json.JSONDecodeError, IOError):
            # Enriched file exists but is invalid, use fallback
            pass
    
    return analysis_file


# ============================================================
# Pipeline Step Implementations
# ============================================================

def run_analyze(repo_path: str, output_file: str) -> None:
    """Pipeline step 1: Static analysis."""
    print("Running static analysis...")
    analysis_result = build_unified_model(repo_path)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analysis_result, f, indent=2)
    
    print("Analysis completed")


def run_enrich(input_file: str, output_file: str, use_llm: bool) -> bool:
    """
    Pipeline step 2: Semantic enrichment (optional).
    
    Returns:
        bool: True if enrichment succeeded, False if it failed (fallback will be used)
    """
    print("\nRunning semantic enrichment...")
    try:
        enrich_file(input_file, output_file, use_llm=use_llm)
        print("Enrichment completed")
        return True
    except Exception as e:
        print(f"Enrichment failed (using fallback): {e}")
        return False


def run_tour(input_file: str, output_file: str) -> None:
    """Pipeline step 3: Guided tour generation."""
    print("\nGenerating tour...")
    result = subprocess.run(
        [sys.executable, "tour/tour_builder.py", input_file],
        check=True,
        capture_output=True,
        text=True
    )
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result.stdout)
    
    print("Tour generated")


def run_flowchart(input_file: str, output_file: str) -> None:
    """Pipeline step 4: Flowchart generation."""
    print("\nGenerating flowchart...")
    subprocess.run(
        [sys.executable, "flowchart/flow_builder.py", input_file, "--output", output_file],
        check=True
    )
    print("Flowchart exported")


# ============================================================
# Pipeline Orchestration
# ============================================================

def run_pipeline(repo_path: str, output_dir: str) -> None:
    """
    Execute the full CODE_Sherpa pipeline in declared order.
    
    Pipeline definition:
        analyze → enrich (optional) → tour → flowchart
    
    This function is the single source of truth for execution order.
    """
    # Define output files (explicit contract)
    analysis_file = os.path.join(output_dir, "analysis.json")
    enriched_file = os.path.join(output_dir, "enriched_analysis.json")
    learning_order_file = os.path.join(output_dir, "learning_order.json")
    flowchart_file = os.path.join(output_dir, "flowchart.md")
    
    # Step 1: Analyze (always runs)
    run_analyze(repo_path, analysis_file)
    
    # Step 2: Enrich (optional, with explicit decision)
    should_run_enrich, use_llm = should_enrich()
    if should_run_enrich:
        enrichment_succeeded = run_enrich(analysis_file, enriched_file, use_llm)
    else:
        enrichment_succeeded = False
    
    # Decision point: Select input file for downstream steps
    # This is explicit, not implicit
    input_for_downstream = select_input_file(analysis_file, enriched_file)
    
    # Step 3: Tour (consumes explicitly selected input)
    run_tour(input_for_downstream, learning_order_file)
    
    # Step 4: Flowchart (consumes explicitly selected input)
    run_flowchart(input_for_downstream, flowchart_file)
    
    print("\nPipeline completed successfully")


# ============================================================
# CLI Entry Point
# ============================================================

def main():
    """CLI entry point. Validates input and delegates to pipeline."""
    if len(sys.argv) < 3:
        print("Usage: python cli/main.py analyze <repo_path>")
        sys.exit(1)
    
    command = sys.argv[1]
    repo_path = sys.argv[2]
    
    if command != "analyze":
        print(f"Unknown command: {command}")
        sys.exit(1)
    
    if not os.path.exists(repo_path):
        print(f"Error: Repository path not found: {repo_path}")
        sys.exit(1)
    
    # Create output directory
    output_dir = "demo"
    os.makedirs(output_dir, exist_ok=True)
    
    # Execute pipeline
    try:
        run_pipeline(repo_path, output_dir)
    except Exception as e:
        print(f"\nPipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
