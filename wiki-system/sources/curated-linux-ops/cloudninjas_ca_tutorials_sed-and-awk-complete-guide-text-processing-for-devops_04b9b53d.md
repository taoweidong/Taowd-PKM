---
source: "https://cloudninjas.ca/tutorials/sed-and-awk-complete-guide-text-processing-for-devops/"
title: "sed and awk Complete Guide: Text Processing for DevOps — CloudNinjas"
fetched_at: "2026-10-06 12:33"
---

VoiceSystem defaultSpeed0.8×1×1.2×1.4×Ready

## Overview

**sed** (stream editor) and **awk** (pattern scanning and processing language) are fundamental text processing tools for Linux systems administrators. This tutorial covers practical implementations of both tools for log analysis, configuration management, and data transformation—critical skills for the Linux Foundation Certified SysAdmin (LFCS) certification.

**Prerequisites:**

  * Basic bash scripting knowledge
  * Understanding of regex patterns
  * Access to a Linux system (Ubuntu, CentOS, or similar)
  * Familiarity with piping and redirection



**Why This Matters for LFCS:** The LFCS exam expects competency in text processing. You'll encounter scenarios requiring log parsing, configuration file modifications, and data extraction—all achievable efficiently with sed and awk.

## Getting Started

Both tools are pre-installed on most Linux distributions. Verify installation:
    
    
    which sed awk
    sed --version
    awk --version

Create a test file for practice:
    
    
    cat > sample.log << 'EOF'
    2024-01-15 10:23:45 ERROR Database connection failed
    2024-01-15 10:24:12 WARNING Low memory condition detected
    2024-01-15 10:25:33 ERROR Authentication timeout
    2024-01-15 10:26:01 INFO Backup completed successfully
    2024-01-15 10:27:19 ERROR Disk space critical
    EOF

## sed: Stream Editing Fundamentals

**sed** processes text line-by-line and applies transformations. The basic syntax is `sed [options] 'command' file`.

**Basic Substitution:**
    
    
    # Replace first occurrence per line
    sed 's/ERROR/CRITICAL/' sample.log
    
    # Replace all occurrences (global flag)
    sed 's/ERROR/CRITICAL/g' sample.log
    
    # Replace on specific lines (lines 1-2)
    sed '1,2s/ERROR/CRITICAL/' sample.log
    
    # Replace on lines matching a pattern
    sed '/WARNING/s/WARNING/CAUTION/g' sample.log

**Deleting Lines:**
    
    
    # Delete lines containing INFO
    sed '/INFO/d' sample.log
    
    # Delete lines 3-4
    sed '3,4d' sample.log
    
    # Delete empty lines
    sed '/^$/d' sample.log

**Inserting and Appending:**
    
    
    # Insert before matching line
    sed '/Database/i\--- LOG SEPARATOR ---' sample.log
    
    # Append after matching line
    sed '/ERROR/a\ACTION: Investigate immediately' sample.log

**Common Pitfall:** sed uses different delimiters for different systems. On macOS, use `sed -i ''` for in-place editing; on Linux, use `sed -i`. Always test with `-i.bak` to create backups first:
    
    
    sed -i.bak 's/ERROR/CRITICAL/g' sample.log

## awk: Pattern Scanning and Processing

**awk** is more powerful than sed—it treats input as records and fields. Basic syntax: `awk 'pattern { action }' file`.

**Field Processing:** awk automatically splits each line into fields ($1, $2, etc.):
    
    
    # Print lines containing ERROR, showing timestamp and message
    awk '/ERROR/ { print $1, $2, $5, $6, $7, $8 }' sample.log
    
    # Print all fields except the first two
    awk '{ $1=$2=""; print }' sample.log
    
    # Extract specific columns
    awk '{ print $1 " | " $3 " | " $5 }' sample.log

**Pattern Matching with Conditions:**
    
    
    # Count ERROR occurrences
    awk '/ERROR/ { count++ } END { print "Total errors: " count }' sample.log
    
    # Print lines where field 3 is ERROR with count
    awk '$3 == "ERROR" { errors++; print } END { print "\nTotal: " errors }' sample.log
    
    # Multiple conditions
    awk '$3 == "ERROR" || $3 == "WARNING" { print $0 }' sample.log

**Advanced Field Manipulation:**
    
    
    # Change field separator and output
    awk -F':' '{ print $1 " uses shell " $NF }' /etc/passwd | head -3
    
    # Set custom output field separator
    awk '{ print $1, $3, $5 }' OFS='|' sample.log
    
    # Calculate string length
    awk '{ print length($0), $0 }' sample.log | sort -rn | head -1

**Built-in Variables:**
    
    
    # NR = Number of Records (line number)
    awk 'NR > 1 && NR <= 3 { print NR ": " $0 }' sample.log
    
    # NF = Number of Fields
    awk '{ print "Line " NR " has " NF " fields" }' sample.log
    
    # FILENAME variable
    awk '{ print FILENAME ": " $0 }' sample.log

**Real-World Example: Log Analysis Script**
    
    
    awk '
    BEGIN { 
        print "=== Log Analysis Report ==="
        errors=0; warnings=0; info=0 
    }
    {
        if ($3 == "ERROR") errors++
        else if ($3 == "WARNING") warnings++
        else if ($3 == "INFO") info++
    }
    END {
        print "Total Errors: " errors
        print "Total Warnings: " warnings
        print "Total Info: " info
        print "Total Lines: " NR
    }
    ' sample.log

## Advanced Techniques: Combining sed and awk

**Pipeline Processing:** Use sed to pre-process, then awk to analyze:
    
    
    # Remove timestamps, then count by severity
    sed 's/^[^ ]* [^ ]* //' sample.log | awk '{ print $1 }' | sort | uniq -c
    
    # Extract errors, remove duplicates, count
    grep ERROR sample.log | sed 's/.*ERROR //' | sort | uniq -c | sort -rn

**Complex Field Operations:**
    
    
    # Parse CSV-like data and calculate averages
    echo -e "user1,cpu,85\nuser1,memory,72\nuser2,cpu,45\nuser2,memory,58" | \
    awk -F',' '{ sum[$1]+=$3; count[$1]++ } END { 
        for (user in sum) print user ": " sum[user]/count[user] "%" 
    }'

**Configuration File Editing with sed:**
    
    
    # Comment out lines containing specific text
    sed 's/^\(.*DEPRECATED.*\)$/#\1/' config.conf
    
    # Replace entire sections
    sed '/^\[OLD_SECTION\]/,/^\[/{ /^\[OLD_SECTION\]/!{ /^\[/!d }; }' config.conf
    
    # Add configuration with line numbers
    cat config.conf | sed -n '10,20p' | nl

## Exam Tips for Linux Foundation Certified SysAdmin (LFCS)

**Key Concepts Tested:**

  * Basic sed substitution with regex patterns
  * awk field extraction and pattern matching
  * Text processing pipelines
  * Log file analysis and filtering
  * Configuration file modifications



**Common Exam Scenarios:**

  1. **Extract data from logs:** "Parse /var/log/auth.log and count failed login attempts" — Use `grep FAILED | wc -l` or `awk '/FAILED/ { count++ }'`
  2. **Modify configuration files:** "Comment out all lines containing 'DEPRECATED'" — Use `sed 's/^\(DEPRECATED.*\)/#\1/'`
  3. **Extract specific columns:** "Show usernames and UIDs from /etc/passwd" — Use `awk -F':' '{ print $1, $3 }'`
  4. **Calculate values:** "Sum disk usage from df output" — Use `awk '{ sum+=$2 } END { print sum }'`



**Quick Reference Commands:**
    
    
    # Delete blank lines
    sed '/^$/d' file
    
    # Case-insensitive substitution
    sed 's/pattern/replacement/i' file
    
    # Print specific range
    sed -n '10,20p' file
    
    # Extract IP addresses
    grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' file
    # Or with awk
    awk -F' ' '{ for(i=1;i<=NF;i++) if($i ~ /^[0-9]+\.[0-9]+/) print $i }' file

## Summary

**Key Takeaways:**

  * **sed** excels at line-by-line text substitution and deletion; use it for quick replacements and file modifications
  * **awk** is superior for field-based processing and complex data extraction; use it for structured data analysis
  * Master regex patterns—they're the foundation for both tools
  * Always test modifications with backups before in-place editing
  * Combine tools in pipelines for powerful text processing workflows



**Next Steps:** Practice with real log files on your system (/var/log/syslog, /var/log/auth.log). Create shell scripts combining sed and awk for log monitoring. Review the LFCS exam objectives focusing on system administration and troubleshooting tasks.

For comprehensive LFCS preparation, explore our Linux Foundation Certified SysAdmin Complete Study Guide covering all exam domains.
