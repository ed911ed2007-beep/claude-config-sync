# Verification Checklist

1. Confirm the three target form XML files are present.
2. Confirm the two reference PPT files are present.
3. Confirm generated PPT can be opened.
4. Unzip PPT and verify Chinese text in slide XML nodes.
5. Confirm backup folder is `backup_YYYY-MM-DD`.
6. Confirm required artifacts exist in backup folder.
7. If validator reports `ModuleNotFoundError: No module named yaml`, run `python -m pip install --user pyyaml`.
8. If validator reports cp950 decode errors on `SKILL.md`, convert `SKILL.md` to system default encoding and re-run validation.
