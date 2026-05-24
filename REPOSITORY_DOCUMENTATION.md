# Project Euler Solutions Repository

## Overview

This repository contains solutions to Project Euler problems, a collection of challenging mathematical/computational problems that require more than just mathematical insights to solve. The repository is designed as both a personal solution archive and a web-accessible code lookup service.

## Repository Statistics

- **Total Solutions**: 152 solution files
- **Language Distribution**:
  - Python: 128 solutions
  - C++: 18 solutions
  - C: 5 solutions
  - Go: 1 solution
- **Problem Range**: Problems 8-940 (selective coverage, not sequential)

## Key Features

### 1. Multi-Language Implementation Strategy

The repository demonstrates polyglot programming with solutions in multiple languages:

- **Python**: Primary language for most solutions, favored for readability and rapid prototyping
- **C++**: Used for performance-critical solutions requiring optimized execution
- **C**: Selected for low-level control and system programming approaches
- **Go**: Experimental usage for certain problem types

### 2. Multiple Implementation Approaches

Several problems feature multiple implementations showcasing different algorithmic approaches:

- **Problem 114**: Both original and dynamic programming (`114_dp.py`) versions
- **Problem 204**: Both Python and C++ implementations
- **Problem 323**: Standard, AI-assisted (`323_ai.py`), and C++ versions
- **Problem 650**: Python, C++, and C implementations
- **Problem 688**: Documented C solution with detailed mathematical notes
- **Problem 719**: Both C and Python implementations
- **Problem 808**: Python and C++ implementations
- **Problem 822**: C implementation with balancing approach
- **Problem 845**: Both C++ and Python implementations
- **Problem 856**: Python and C++ implementations
- **Problem 918**: Python, C++, and AI-assisted C++ versions

### 3. FastAPI Web Service

The repository includes a fully functional FastAPI web service (`api.py`) that provides:

#### Core Functionality
- **Code Lookup API**: RESTful endpoints to retrieve solutions by problem number
- **Language Filtering**: Optional filtering by programming language
- **Interactive Web Interface**: Beautiful, responsive HTML frontend for code browsing

#### API Endpoints
- `GET /` - Interactive web interface for manual code lookup
- `GET /health` - Health check endpoint
- `GET /problems/{problem_number}` - Retrieve solution(s) for a specific problem
  - Query parameter: `?language={python|cpp|c|go}` for language filtering

#### Web Interface Features
- Elegant, responsive design with custom CSS
- Problem number input and language selection
- Syntax-highlighted code display
- One-click code copying functionality
- Real-time feedback and error handling

### 4. Production Deployment Configuration

The repository includes complete systemd service configuration for production deployment:

#### HTTP Service (`euler-api.service`)
- Runs on localhost:8000
- Auto-restart on failure
- Unbuffered Python output
- User-level systemd service

#### HTTPS Service (`euler-api-https.service`)
- Runs on 0.0.0.0:8443 for network accessibility
- SSL/TLS encryption with configurable certificates
- Certificate storage in `~/.config/euler-api/tls/`
- Supports local CA trust configuration for LAN access

### 5. Documentation and Code Quality

#### Inline Documentation
- Comprehensive file headers with Project Euler URLs
- Algorithm descriptions and mathematical explanations
- Performance notes and complexity analysis
- Input/output format specifications

#### Code Organization Patterns
- Consistent naming convention: `{problem_number}.{extension}`
- Support files: `{problem_number}.input`, `{problem_number}.txt` for test data
- Variant implementations: `{problem_number}_{variant}.{extension}` (e.g., `114_dp.py`, `323_ai.py`)

#### Development Practices
- Recent refactoring efforts (e.g., "Refactor solution for problem 509")
- Documentation additions (e.g., "Add documented solution for problem 688")
- Code formatting with Black Python formatter
- Performance optimization and timing additions
- Algorithm rewrite improvements (e.g., "Rewrite 822.c using balancing approach")

### 6. Advanced Algorithmic Techniques

The solutions demonstrate various computational approaches:

#### Dynamic Programming
- Problem 114: State machine DP for tile counting
- Problem 509: Grundy number analysis for game theory

#### Mathematical Optimization
- Problem 688: Arithmetic series optimization for large-scale computation
- Problem 323: Inclusion-exclusion principle with high-precision arithmetic
- Problem 509: Modular arithmetic with bucket counting

#### Performance-Critical Implementations
- C/C++ solutions for problems requiring optimized execution
- Use of 128-bit integers for overflow prevention
- Efficient memory management and algorithmic complexity optimization

### 7. Development Infrastructure

#### Dependencies
- **FastAPI** (≥0.110, <1.0): Modern Python web framework
- **Uvicorn** (≥0.29, <1.0): ASGI server for FastAPI deployment

#### Development Tools
- VS Code workspace configuration (`euler.code-workspace`)
- Git version control with detailed commit history
- Devin CLI configuration for AI-assisted development

### 8. Problem Coverage and Special Cases

#### Input Data Files
Several problems include dedicated input data files:
- `11.input`: 20x20 grid data for Problem 11
- `13.input`: Large number data for Problem 13
- `18.txt`: Triangle data for Problem 18
- `22.txt`: Name data for Problem 22
- `79.txt`: Data for Problem 79

#### Visual Assets
- `940.png`: Visual reference for Problem 940

#### Special Implementations
- `18_and_67.cpp`: Combined solution for Problems 18 and 67 (same algorithm)
- `59.y`: YAML-based solution (experimental format)

## Code Style and Conventions

### Python Solutions
- Shebang line: `#!/usr/bin/env python3`
- Docstrings with Project Euler URLs
- Direct script execution with `if __name__ == "__main__":`
- Input reading via `input()` for interactive problems
- Print-based output for results

### C++ Solutions
- Standard iostream usage
- STL containers (vector, etc.)
- Type-safe implementations with proper includes
- Clear algorithmic structure with nested loops

### C Solutions
- Standard library usage (stdio.h, time.h, etc.)
- Performance-oriented implementations
- Modular functions with clear separation of concerns
- Timing instrumentation for performance measurement

## Recent Development Activity

Based on git history, recent development focuses on:
1. **Refactoring**: Improving existing solution implementations
2. **Documentation**: Adding comprehensive explanations and comments
3. **Cross-language Implementation**: Adding C/C++ versions of Python solutions
4. **Performance Optimization**: Algorithm improvements and timing additions
5. **Infrastructure**: Web service development and deployment configuration

## Usage Examples

### Running Individual Solutions
```bash
# Python solution
python3 8.py < 8.input

# C++ solution
g++ -o 11 11.cpp && ./11 < 11.input

# C solution
gcc -o 688 688.c && ./688
```

### Running the Web Service
```bash
# Install dependencies
python3 -m pip install -r requirements.txt

# Development server
uvicorn api:app --reload

# Production server
.venv/bin/uvicorn api:app --host 0.0.0.0 --port 8000

# HTTPS server
.venv/bin/uvicorn api:app --host 0.0.0.0 --port 8443 \
  --ssl-keyfile ~/.config/euler-api/tls/euler-local-server.key \
  --ssl-certfile ~/.config/euler-api/tls/euler-local-server.crt
```

### API Usage
```bash
# Get all implementations for problem 8
curl http://127.0.0.1:8000/problems/8

# Get only Python implementation
curl "http://127.0.0.1:8000/problems/204?language=python"

# Health check
curl http://127.0.0.1:8000/health
```

### Systemd Service Installation
```bash
# Install HTTP service
mkdir -p ~/.config/systemd/user
cp euler-api.service ~/.config/systemd/user/euler-api.service
systemctl --user daemon-reload
systemctl --user enable --now euler-api.service

# Install HTTPS service (with certificates in place)
cp euler-api-https.service ~/.config/systemd/user/euler-api-https.service
systemctl --user daemon-reload
systemctl --user enable --now euler-api-https.service
```

## Technical Highlights

### Algorithmic Sophistication
- Game theory applications (Grundy numbers, impartial games)
- Number theory optimizations (modular arithmetic, prime factorization)
- Dynamic programming state machines
- Inclusion-exclusion principle applications
- High-precision decimal arithmetic
- Combinatorial mathematics

### Performance Engineering
- Language selection based on performance requirements
- Algorithm complexity optimization
- Memory-efficient data structures
- Overflow prevention with extended integer types
- Timing and performance measurement

### Software Engineering Practices
- RESTful API design
- Responsive web development
- Systemd service configuration
- SSL/TLS deployment
- Cross-language interoperability
- Comprehensive documentation

## Conclusion

This repository represents a sophisticated approach to Project Euler problem solving, combining mathematical insight with software engineering best practices. It serves as both a personal archive of algorithmic solutions and a production-ready web service for code lookup and reference. The multi-language approach, comprehensive documentation, and deployment infrastructure make it a valuable resource for studying both mathematical problem-solving and modern software development practices.