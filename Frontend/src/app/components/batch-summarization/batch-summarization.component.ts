import { Component, inject } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-batch-summarization',
  templateUrl: './batch-summarization.component.html',
  styleUrl: './batch-summarization.component.css'
})
export class BatchSummarizationComponent {
  fileSelected = false;
  fileName: string | null = null;
  isLoading = false;
  isSummarized = false;
  toastr : ToastrService = inject(ToastrService);

  // Triggered when a file is selected
  onFileSelect(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.fileSelected = true;
      this.fileName = file.name; // Display the file name
    }
  }
  // Triggered when a file is dropped
  onFileDrop(event: DragEvent) {
    event.preventDefault();
    const file = event.dataTransfer?.files[0];
    if (file) {
      this.fileSelected = true;
      this.fileName = file.name; // Display the file name
    }
  }
  // Prevents default behavior on dragover
  onDragOver(event: DragEvent) {
    event.preventDefault();
  }
  // Simulate summarization process
  summarizeFile() {
    this.isLoading = true;
    this.isSummarized = false;
    // Simulating a delay for summarization
    setTimeout(() => {
      this.toastr.success('Summarization Process Completed', 'Success...👍', {
        timeOut: 30000,
      });


      this.isLoading = false;
      this.isSummarized = true;

    }, 3000);
  }
  // Clear the selected file
  clearFile() {
    this.fileSelected = false;
    this.fileName = null;
    this.isSummarized = false;
    this.isLoading = false;
  }
  // Export functionality
  exportCsv() {
    console.log('Exporting CSV...');
  }


}
