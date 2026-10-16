/**
 * OpenCode 1.x plugin: after edit/write of project files, run trusted test runner
 * and append stdout/stderr to the tool result for the agent.
 */
export const CheckAfterEditPlugin = async ({ $, directory }) => {
  return {
    "tool.execute.after": async (input, output) => {
      if (!output) return
      const tool = input.tool
      if (tool !== "edit" && tool !== "write" && tool !== "apply_patch") return

      const path = String(
        (input.args && (input.args.path || input.args.filePath)) ||
          (output.metadata && output.metadata.path) ||
          "",
      )
      if (path && !path.endsWith(".py") && !path.endsWith("Makefile")) return

      try {
        const result = await $`python scripts/check.py`.cwd(directory).nothrow()
        const stdout = result.stdout?.toString?.() ?? String(result.stdout ?? "")
        const stderr = result.stderr?.toString?.() ?? String(result.stderr ?? "")
        const block = [
          "",
          "--- hook check-after-edit: python scripts/check.py ---",
          stdout,
          stderr,
          `exit: ${result.exitCode}`,
          "--- end hook ---",
          "",
        ].join("\n")
        output.title = `${output.title || tool} (+tests)`
        output.output = `${output.output || ""}${block}`
      } catch (err) {
        output.output = `${output.output || ""}\nhook failed: ${err}`
      }
    },
  }
}

export default CheckAfterEditPlugin
