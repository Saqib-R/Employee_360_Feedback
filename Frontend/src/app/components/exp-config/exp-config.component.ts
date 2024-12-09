import { Component } from '@angular/core';

@Component({
  selector: 'app-exp-config',
  templateUrl: './exp-config.component.html',
  styleUrl: './exp-config.component.css'
})
export class ExpConfigComponent {
  jobRoles: string[] = ['Senior Frontend Developer', 'Backend Developer', 'Project Manager']; // Add more roles as needed
  selectedJobRole: string | null = null;
  expectations: string = '';
  customPromptTitle: string = '';
  customPromptContent: string = '';

  onJobRoleChange() {
    this.expectations = ''; // Clear expectations when a new job role is selected
  }

  generateWithAI() {
    // Add logic to generate expectations using AI
    console.log(`Generating expectations for ${this.selectedJobRole}`);
  }

  saveExpectations() {
    // Save expectations logic
    console.log(`Expectations saved for ${this.selectedJobRole}: ${this.expectations}`);
  }

  generateCustomAI() {
    // Add logic to generate custom prompts using AI
    console.log(`Generating custom prompt: ${this.customPromptTitle}`);
  }

  saveCustomPrompt() {
    // Save custom prompt logic
    console.log(`Custom prompt saved: ${this.customPromptTitle} - ${this.customPromptContent}`);
  }

  onFileUpload(event: any) {
    const file = event.target.files[0];
    if (file) {
      console.log('Uploaded file:', file.name);
      // Add logic to parse and handle CSV file
    }
  }

}
