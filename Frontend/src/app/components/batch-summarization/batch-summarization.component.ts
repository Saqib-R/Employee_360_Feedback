import { Component } from '@angular/core';

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
    // Simulate a delay for summarization (replace with actual summarization logic)
    setTimeout(() => {
      this.isLoading = false;
      this.isSummarized = true; // Enable export button after summarization is done
    }, 3000); // Adjust time as needed
  }
  // Clear the selected file
  clearFile() {
    this.fileSelected = false;
    this.fileName = null; // Reset file name
    this.isSummarized = false;
    this.isLoading = false;
  }
  // Simulate CSV export functionality
  exportCsv() {
    console.log('Exporting CSV...');
    // Implement your CSV export logic here
  }

  ngOnChanges(): void {
    //Called before any other lifecycle hook. Use it to inject dependencies, but avoid any serious work here.
    //Add '${implements OnChanges}' to the class.
    console.log("Loading Value : \t", this.isLoading, "\nSummarise Value : \t", this.isSummarized);
  }

}
