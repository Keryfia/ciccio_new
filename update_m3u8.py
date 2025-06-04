name: Update M3U8 Links

on:
  workflow_dispatch:
    inputs:
      old_domain:
        description: 'Dominio da sostituire'
        required: true
        default: 'keryfia-newale.hf.space'
        type: string
      new_domain:
        description: 'Nuovo dominio'
        required: true
        type: string
      commit_message:
        description: 'Messaggio del commit'
        required: false
        default: 'Update M3U8 links'
        type: string

jobs:
  update-links:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Update M3U8 links
      run: |
        python update_m3u8.py --old "${{ github.event.inputs.old_domain }}" --new "${{ github.event.inputs.new_domain }}"
        
    - name: Check for changes
      id: check_changes
      run: |
        if git diff --quiet; then
          echo "changes=false" >> $GITHUB_OUTPUT
        else
          echo "changes=true" >> $GITHUB_OUTPUT
        fi
        
    - name: Commit and push changes
      if: steps.check_changes.outputs.changes == 'true'
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add listone.m3u8
        git commit -m "${{ github.event.inputs.commit_message }}: ${{ github.event.inputs.old_domain }} → ${{ github.event.inputs.new_domain }}"
        git push
        
    - name: No changes detected
      if: steps.check_changes.outputs.changes == 'false'
      run: |
        echo "ℹ️ Nessuna modifica da committare. Il dominio potrebbe essere già aggiornato."
