import { Component, ElementRef, inject, ViewChild } from '@angular/core';
import { UploadService } from '../../services/upload.service';
import { ToastrService } from 'ngx-toastr';

// Structured Response Interface
interface StructuredResponse {
  job_title: string;
  attributes: { attribute_name: string; expectations: string[] }[];
}

// Chat Message Interface
interface ChatMessage {
  text: string;
  response: StructuredResponse;
}

@Component({
  selector: 'app-chat-bot',
  templateUrl: './chat-bot.component.html',
  styleUrl: './chat-bot.component.css'
})
export class ChatBotComponent {
  userInput: string = '';
  // chatMessages: {
  //   text: string;
  //   response: {
  //     job_title: string;
  //     attributes: {
  //       attribute_name: string;
  //       expectations: string[];
  //     }[];
  //   };
  // }[] = [];
  chatMessages: { text: string; response: { [key: string]: string[] } | null }[] = [];
  isLoading: boolean = false;
  chatService : UploadService = inject(UploadService)
  toastr : ToastrService = inject(ToastrService)
  objectKeys = Object.keys;

  sendMessage() {
    if (!this.userInput.trim()) return;

    const userMessage = this.userInput;
    this.chatMessages.push({ text: userMessage, response: null });
    this.userInput = '';

    // Simulate bot response
    this.isLoading = true;
    this.chatService.promptRag(userMessage).subscribe({
      next: (res) => {
        console.log("Chatbot Response...",res);
        this.chatMessages[this.chatMessages.length - 1].response = res.data;
        console.log("CHAT ", this.chatMessages[this.chatMessages.length - 1]);

        this.isLoading = false;
      },
      error: (err) => {
        console.log(err);
      }
    })

    // setTimeout(() => {
    //   const botResponse = this.generateBotResponse(userMessage);
    //   // this.chatMessages[this.chatMessages.length - 1].response = botResponse;
    //   this.isLoading = false;
    // }, 1000);
  }

  // Clear Chat
  clearChat() {
    this.chatMessages = [];
  }

  // Generate bot response (mock)
  private generateBotResponse(userMessage: string): string {
    return `You said: "${userMessage}". How can I assist further?`;
  }

  @ViewChild('chatContainer') chatContainer!: ElementRef;

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  scrollToBottom(): void {
    if (this.chatContainer) {
      this.chatContainer.nativeElement.scrollTop = this.chatContainer.nativeElement.scrollHeight;
    }
  }


}
