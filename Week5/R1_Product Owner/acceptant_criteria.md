# Acceptance Criteria 

The Sprint 5 integrated pipeline is considered complete when:

1. Market data is collected and stored in a structured format.
2. Almanac (R3), Macro (R4), and Technical (R5) outputs are committed before LLM synthesis begins.
3. ChatGPT, Gemini, and DeepSeek responses are saved and committed by R8.
4. Human Score / Wild Card analysis is included in the final prediction process.
5. prediction_W25.json is generated successfully and contains directional predictions, confidence, and Human Score input.
6. Automated fetch evidence is available through GitHub Actions or an approved equivalent process.
7. README or pipeline documentation clearly shows the end-to-end workflow from market close to prediction seal.
8. All role outputs contribute to the final prediction file.
9. The pipeline can run end-to-end with minimal human intervention.
10. The repository is ready for vW25 release tagging.

## Product Owner Sign-off

The integrated pipeline will be accepted when all required role outputs are connected into a single prediction workflow and the system can operate from data collection to sealed prediction with minimal human intervention.

README Status: Pending final review.

Pipeline Coherence Status: Pending verification before vW25 release.

Final W25 Call: To be confirmed during final review.
