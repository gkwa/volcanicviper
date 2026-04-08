---
name: solid-principles
description: Write code following SOLID design principles with good information hiding. Use when writing or reviewing code for architecture, class design, or module organization.
---

Follow SOLID design principles and maintain good information hiding:

1. Single Responsibility Principle (SRP): A class should have only one reason to change.
2. Open-Closed Principle (OCP): Open for extension, closed for modification.
3. Liskov Substitution Principle (LSP): Subclass objects should be substitutable for superclass objects.
4. Interface Segregation Principle (ISP): Many client-specific interfaces are better than one general-purpose interface.
5. Dependency Inversion Principle (DIP): High-level modules should not depend on low-level modules — both should depend on abstractions.

Individual code files should strive to stay under 200 lines. This is a goal, not a strict limit — justified outliers are fine.

Decompose extensive logic into multiple discrete files rather than accumulating lines in a single file. This promotes information hiding and keeps modules focused and comprehensible.

When writing code, consider:
- Does it adhere to SOLID principles? If not, which principles are being violated?
- Is the code organized into small, focused units?
- Are there areas where information hiding could be improved?
