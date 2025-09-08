# French Tax MCP Server - Refactoring Tasks
## Goal: Remove Enterprise Functionality & Keep Only Income Particulier Part

**Project Status**: Starting refactoring to focus only on individual income tax calculations
**Date Started**: 2025-01-08
**Current Phase**: Analysis and Planning

---

## TASK BREAKDOWN

### PHASE 1: ANALYSIS AND CLEANUP PREPARATION

#### Task 1.1: Analyze Current Enterprise Dependencies
**Status**: COMPLETED ✅
**Priority**: HIGH
**Description**: 
- Analyze all files that contain enterprise/business functionality
- Identify which tools/functions are enterprise-related vs individual income related
- Map dependencies between enterprise and individual functionality
- Create list of files/functions to remove vs keep

**Files to analyze**:
- `french_tax_mcp/analyzers/business_analyzer.py` (REMOVE)
- `french_tax_mcp/analyzers/property_analyzer.py` (REMOVE - Pinel/LMNP are investment/business)
- `french_tax_mcp/analyzers/income_analyzer.py` (KEEP - individual income tax)
- `french_tax_mcp/server.py` (MODIFY - remove enterprise tools)
- `french_tax_mcp/constants.py` (MODIFY - remove enterprise constants)

**Acceptance Criteria**:
- Complete list of files to remove
- Complete list of functions to remove from remaining files
- Dependency map showing what can be safely removed
- No breaking changes to individual income functionality

**Developer Instructions**:
1. Open each file in the analyzers directory
2. Read through all functions and identify which are for:
   - Individual income tax (KEEP)
   - Business/enterprise tax (REMOVE)
   - Property investment tax (REMOVE - Pinel, LMNP)
3. Check server.py for all tool registrations
4. Document findings in this file under "Analysis Results"

---

#### Task 1.2: Identify Individual Income Tax Core Functions
**Status**: COMPLETED ✅  
**Priority**: HIGH
**Description**:
Identify and document the core functions that MUST be preserved for individual income tax calculations.

**Core functions to preserve**:
- `calculate_income_tax()` - Main individual income tax calculation
- `get_tax_brackets()` - Tax brackets for progressive taxation
- Individual tax form information (2042, not business forms)
- Individual tax deadlines and procedures

**Files to examine**:
- `french_tax_mcp/analyzers/income_analyzer.py`
- `french_tax_mcp/scrapers/` (identify individual vs business scrapers)
- `french_tax_mcp/server.py` (identify individual vs business tools)

**Acceptance Criteria**:
- List of core individual income functions documented
- Verification that these functions don't depend on enterprise code
- Test plan for validating individual income calculations still work

---

### PHASE 2: REMOVE ENTERPRISE FUNCTIONALITY

#### Task 2.1: Remove Business Analyzer Module
**Status**: COMPLETED ✅
**Priority**: HIGH  
**Description**:
Completely remove the business_analyzer.py module and all its dependencies.

**Changes to make**:
1. Delete `french_tax_mcp/analyzers/business_analyzer.py`
2. Remove business_analyzer imports from `server.py`
3. Remove business-related tools from server.py:
   - `calculate_micro_enterprise_tax` tool
   - Any other business calculation tools
4. Update `analyzers/__init__.py` to remove business_analyzer exports

**Files to modify**:
- DELETE: `french_tax_mcp/analyzers/business_analyzer.py`
- MODIFY: `french_tax_mcp/server.py` (remove imports and tools)
- MODIFY: `french_tax_mcp/analyzers/__init__.py`

**Acceptance Criteria**:
- business_analyzer.py file deleted
- No imports of business_analyzer in any file
- No business calculation tools in server.py
- Server starts without errors
- Individual income tools still work

**Developer Instructions**:
1. First, identify all places business_analyzer is imported
2. Remove the import statements
3. Remove any tool registrations that use business_analyzer functions
4. Delete the business_analyzer.py file
5. Test that server starts: `uv run python -m french_tax_mcp.server`

---

#### Task 2.2: Remove Property Analyzer Module  
**Status**: COMPLETED ✅
**Priority**: HIGH
**Description**:
Remove property_analyzer.py module containing Pinel and LMNP investment calculations (these are business/investment, not individual income).

**Changes to make**:
1. Delete `french_tax_mcp/analyzers/property_analyzer.py`
2. Remove property_analyzer imports from `server.py`
3. Remove property-related tools from server.py:
   - `calculate_pinel_benefit` tool
   - `calculate_lmnp_benefit` tool
4. Update `analyzers/__init__.py`

**Files to modify**:
- DELETE: `french_tax_mcp/analyzers/property_analyzer.py`
- MODIFY: `french_tax_mcp/server.py`
- MODIFY: `french_tax_mcp/analyzers/__init__.py`

**Acceptance Criteria**:
- property_analyzer.py file deleted
- No property investment tools in server
- Server starts without errors
- Individual income calculations unaffected

---

#### Task 2.3: Clean Up Constants File
**Status**: COMPLETED ✅
**Priority**: MEDIUM
**Description**:
Remove all enterprise/business-related constants from constants.py, keeping only individual income tax constants.

**Constants to REMOVE**:
- Micro-enterprise rates and thresholds
- Pinel investment rates and limits  
- LMNP/LMP constants
- Business form URLs
- Any business-specific tax brackets or rates

**Constants to KEEP**:
- Individual income tax brackets (TAX_BRACKETS)
- Individual tax form URLs (2042, etc.)
- Service-public.fr URLs for individual procedures
- Individual tax deadlines

**Files to modify**:
- MODIFY: `french_tax_mcp/constants.py`

**Acceptance Criteria**:
- Only individual income tax constants remain
- No business/enterprise constants
- Individual income calculations still work with remaining constants
- File is clean and well-organized

---

### PHASE 3: IMPLEMENT DYNAMIC DATA FETCHING

#### Task 3.1: Integrate MarkItDown Scraper for Tax Brackets
**Status**: COMPLETED ✅
**Priority**: HIGH
**Description**:
Replace hardcoded tax brackets with dynamic fetching using MarkItDown scraper.

**Changes to make**:
1. Integrate the MarkItDown scraper we created earlier
2. Modify `get_tax_brackets()` function to use MarkItDown scraper as primary source
3. Keep hardcoded brackets as fallback only
4. Add proper error handling and logging

**Files to modify**:
- ADD: `french_tax_mcp/scrapers/markitdown_scraper.py` (already created)
- MODIFY: `french_tax_mcp/scrapers/service_public_scraper.py` or create new integration
- MODIFY: Functions that call get_tax_brackets()

**Acceptance Criteria**:
- Tax brackets fetched dynamically from service-public.fr
- Hardcoded brackets used only as fallback
- Proper error handling when scraping fails
- Tax calculations use live data when available

---

#### Task 3.2: Update Income Tax Calculation to Use Dynamic Data
**Status**: COMPLETED ✅
**Priority**: HIGH
**Description**:
Modify the income tax calculation to use dynamically fetched tax brackets instead of hardcoded ones.

**Changes to make**:
1. Update `calculate_income_tax()` in income_analyzer.py
2. Make it call dynamic tax bracket fetching first
3. Fall back to hardcoded data only if scraping fails
4. Add logging to show data source used

**Files to modify**:
- MODIFY: `french_tax_mcp/analyzers/income_analyzer.py`

**Acceptance Criteria**:
- Income tax calculations use live tax brackets when available
- Fallback to hardcoded data works correctly
- Clear logging shows which data source was used
- Calculation accuracy maintained

---

### PHASE 4: TESTING AND VALIDATION

#### Task 4.1: Test Individual Income Tax Functionality
**Status**: COMPLETED ✅
**Priority**: HIGH
**Description**:
Comprehensive testing of remaining individual income tax functionality after enterprise removal.

**Tests to perform**:
1. Test `calculate_income_tax` tool with various income levels
2. Test `get_tax_brackets` tool for current year
3. Test dynamic data fetching vs fallback behavior
4. Verify server starts and responds correctly
5. Test error handling when scraping fails

**Acceptance Criteria**:
- All individual income tax tools work correctly
- Dynamic data fetching works
- Fallback to hardcoded data works
- No errors or broken functionality
- Server performance is acceptable

---

#### Task 4.2: Clean Up Unused Files and Dependencies
**Status**: TODO
**Priority**: MEDIUM
**Description**:
Remove any unused files, imports, or dependencies after enterprise functionality removal.

**Cleanup tasks**:
1. Remove unused scraper files (if any are business-only)
2. Clean up unused imports in remaining files
3. Update requirements/dependencies if any are no longer needed
4. Remove unused constants or helper functions
5. Update documentation/README to reflect individual-only focus

**Files to review**:
- All remaining Python files for unused imports
- `pyproject.toml` for unused dependencies
- Documentation files

**Acceptance Criteria**:
- No unused imports or dead code
- Clean, minimal codebase focused on individual income tax
- Updated documentation
- No unnecessary dependencies

---

## ANALYSIS RESULTS

### Enterprise vs Individual Function Analysis
**COMPLETED - Task 1.1**

**FILES TO REMOVE COMPLETELY:**
- `french_tax_mcp/analyzers/business_analyzer.py` - Contains micro-enterprise tax calculations
- `french_tax_mcp/analyzers/property_analyzer.py` - Contains Pinel/LMNP investment calculations

**FILES TO KEEP (Individual Income Only):**
- `french_tax_mcp/analyzers/income_analyzer.py` - Individual income tax calculations ✅

**FILES TO MODIFY:**
- `french_tax_mcp/server.py` - Remove business/property imports and tools
- `french_tax_mcp/constants.py` - Remove business/property constants
- `french_tax_mcp/analyzers/__init__.py` - Remove business/property exports

**IMPORTS TO REMOVE FROM server.py:**
```python
from french_tax_mcp.analyzers.business_analyzer import calculate_micro_enterprise_tax
from french_tax_mcp.analyzers.property_analyzer import (
    calculate_lmnp_benefit,
    calculate_pinel_benefit,
)
```

### Core Individual Functions Identified  
**COMPLETED - Task 1.2**

**FUNCTIONS TO KEEP:**
- `calculate_income_tax()` - Main individual income tax calculation
- `get_tax_brackets()` - Tax brackets for progressive taxation
- Individual tax form scrapers (2042 forms)
- Individual tax procedure scrapers

---

## CHANGE LOG
*All changes will be documented here with reasons*

### Changes Made

#### Task 2.1 - Remove Business Analyzer Module (COMPLETED ✅)
**Date**: 2025-01-08
**Changes**:
1. ✅ DELETED: `french_tax_mcp/analyzers/business_analyzer.py`
2. ✅ REMOVED: Import `from french_tax_mcp.analyzers.business_analyzer import calculate_micro_enterprise_tax` from server.py
3. ✅ REMOVED: `calculate_micro_enterprise_tax` tool and wrapper function from server.py
4. ✅ VERIFIED: `analyzers/__init__.py` had no business_analyzer exports to remove

#### Task 2.2 - Remove Property Analyzer Module (COMPLETED ✅)
**Date**: 2025-01-08
**Changes**:
1. ✅ DELETED: `french_tax_mcp/analyzers/property_analyzer.py`
2. ✅ REMOVED: Import `from french_tax_mcp.analyzers.property_analyzer import (calculate_lmnp_benefit, calculate_pinel_benefit)` from server.py
3. ✅ VERIFIED: No Pinel/LMNP tools found in server.py (already removed)

**Reason**: Removing all property investment functionality (Pinel, LMNP) to focus only on individual income tax calculations.

#### Task 2.2 Testing Results
**Test Command**: `uv run python -c "from french_tax_mcp.server import mcp; print('✅ Server imports successfully after property removal')"`
**Result**: ✅ SUCCESS - No compilation errors

#### Task 2.3 - Clean Up Constants File (COMPLETED ✅)
**Date**: 2025-01-08
**Changes**:
1. ✅ REMOVED: All PINEL constants (rates, max investment, price per m²)
2. ✅ REMOVED: All MICRO_ENTERPRISE constants (abatement rates, social charges, thresholds)
3. ✅ REMOVED: All LMNP constants (depreciation, thresholds, professional limits)
4. ✅ REMOVED: ACCRE and VERSEMENT_LIBERATOIRE constants
5. ✅ KEPT: TAX_BRACKETS (individual income tax brackets)
6. ✅ KEPT: HOUSEHOLD_PARTS constants (quotient familial for individual tax)
7. ✅ KEPT: TAX_FORMS (individual tax forms like 2042)

**Reason**: Removed all business/property investment constants, keeping only individual income tax calculation constants.

#### Task 2.3 Testing Results
**Test Command**: `uv run python -c "from french_tax_mcp.server import mcp; print('✅ Server imports successfully after constants cleanup')"`
**Result**: ✅ SUCCESS - No compilation errors

### Compilation Errors Fixed

#### Task 2.1 Testing Results
**Date**: 2025-01-08
**Test Command**: `uv run python -c "from french_tax_mcp.server import mcp; print('✅ Server imports successfully')"`
**Result**: ✅ SUCCESS - No compilation errors
**Output**: Server imports successfully with normal scraper initialization logs

---

## DECISIONS MADE
*All decisions and approvals will be recorded here*

### Decision Log
*Format: [Date] [Task] [Decision] [Reason]*

---

## TESTING RESULTS
*Results of testing after each major change*

### Test Results Log
*To be filled during Phase 4*
