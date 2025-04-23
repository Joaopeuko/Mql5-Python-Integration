#!/usr/bin/env python
"""Generate the API reference pages for the MQPy package."""

import os
import sys
from pathlib import Path

import mkdocs_gen_files

# Add the project root to the Python path so we can import mqpy
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

package_dir = project_dir / "mqpy"
package_name = "mqpy"

# Create a navigation structure
nav = mkdocs_gen_files.Nav()

# Ensure the reference directory exists
os.makedirs(project_dir / "docs" / "reference", exist_ok=True)

# Create an index page with a better layout
index_path = Path("reference", "index.md")
with mkdocs_gen_files.open(index_path, "w") as index_file:
    index_file.write("# API Reference\n\n")
    index_file.write(f"This section contains the complete API reference for all public modules and classes in {package_name}.\n\n")
    index_file.write("## Available Modules\n\n")

# Create documentation for each module
for path in sorted(package_dir.glob("**/*.py")):
    module_path = path.relative_to(project_dir).with_suffix("")
    doc_path = path.relative_to(project_dir).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)
    
    # Skip __init__.py and __main__.py for individual pages
    parts = module_path.parts
    if parts[-1] in ["__init__", "__main__"]:
        continue
    
    # Generate proper import path
    import_path = ".".join(parts)
    
    # Create directory for the documentation
    os.makedirs(full_doc_path.parent, exist_ok=True)
    
    # Write the page content - customized to skip module headers
    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        # Instead of directly using the main import path, create a custom approach
        # that doesn't show the module header but still shows classes and functions
        # fd.write("---\nhide:\n  - toc\n---\n\n")
        fd.write("<!-- Auto-generated API documentation -->\n\n")
        
        # # Write documentation for classes and functions instead of the module
        # # This approach avoids generating the module header while still including all content
        fd.write(f"::: {import_path}\n")
    # Add to navigation
    nav[parts] = doc_path.as_posix()
    
    # Update index file with simple links
    with mkdocs_gen_files.open(index_path, "a") as index_file:
        rel_path = doc_path.as_posix()
        module_name = parts[-1]
        index_file.write(f"- [{module_name}]({rel_path})\n")

# Generate and write the navigation file
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.write("# API Reference\n\n")
    nav_file.writelines(nav.build_literate_nav())
