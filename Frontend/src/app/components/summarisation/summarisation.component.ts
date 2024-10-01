import { Component } from '@angular/core';

@Component({
  selector: 'app-summarisation',
  templateUrl: './summarisation.component.html',
  styleUrl: './summarisation.component.css'
})
export class SummarisationComponent {

  question: string = "How does Jane Doe handle complex tasks?";
  summaryResponse: string = "Jane consistently demonstrates strong problem-solving skills in handling complex tasks. Jane consistently demonstrates strong problem-solving skills in handling complex tasks. Jane consistently demonstrates strong problem-solving skills in handling complex tasks";
  promptInput: string = '';

  // Function to handle prompt submission
  submitPrompt() {
    console.log('Prompt submitted: ', this.promptInput);
    // Lama response will get it later
  }

  // Adjusting textarea height dynamically
  adjustTextareaHeight(event: any) {
    const textarea = event.target;
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
  }

  // Tracking whether the summary is expanded or not
  isExpanded: boolean = false;
  // Toggle expand/collapse state
  toggleSummary() {
    this.isExpanded = !this.isExpanded;
    const summaryText = document.querySelector('.summary-text');
    const toggleIcon = document.querySelector('.summary-toggle i');
    if (this.isExpanded) {
      summaryText?.setAttribute('style', 'max-height: none');
      toggleIcon?.classList.add('collapsed');
    } else {
      summaryText?.setAttribute('style', 'max-height: 100px');
      toggleIcon?.classList.remove('collapsed');
    }
  }

}
