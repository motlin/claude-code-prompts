# Tab Color Configuration

Configure a terminal tab color for the current project using direnv.

## Arguments

The user provided: $ARGUMENTS

This should be a color description like "yellow", "blue", "red", "orange", "purple", "green", "pink", "cyan", "amber", etc.

## Instructions

1. Convert the color description to an RGB value.

2. Check if `.envrc` already exists in the current directory:
   - If it exists, read it and add/update the `TAB_COLOR` export
   - If it doesn't exist, create it with just the `TAB_COLOR` export

3. The format should be:
   ```
   export TAB_COLOR='R,G,B'
   ```

Example: export TAB_COLOR='41,56,140'

4. After creating/updating the file, run `direnv allow` to enable it

5. Report the RGB value used and confirm the setup is complete
