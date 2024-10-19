import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AppComponent } from './app.component';
import { UploadService } from './services/upload.service';
import { NavbarComponent } from './components/navbar/navbar.component';
import { HomeComponent } from './components/home/home.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { ViewFeedbacksComponent } from './components/view-feedbacks/view-feedbacks.component';
import { UploadCSVComponent } from './components/upload-csv/upload-csv.component';
import { FeedbackAccordianComponent } from './components/feedback-accordian/feedback-accordian.component';
import { SummarisationComponent } from './components/summarisation/summarisation.component';
import { NoFeedbacksComponent } from './components/no-feedbacks/no-feedbacks.component';
import { BatchSummarizationComponent } from './components/batch-summarization/batch-summarization.component';
import { CommonModule } from '@angular/common';
import { ToastrModule } from 'ngx-toastr';
import { FormsModule } from '@angular/forms';
import { LoginComponent } from './components/login/login.component';
import { EmployeeOverviewComponent } from './components/employee-overview/employee-overview.component';
import { EmpAccordianComponent } from './components/emp-accordian/emp-accordian.component';
import { EmpAccordianCardComponent } from './components/emp-accordian-card/emp-accordian-card.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    HomeComponent,
    ViewFeedbacksComponent,
    UploadCSVComponent,
    FeedbackAccordianComponent,
    SummarisationComponent,
    NoFeedbacksComponent,
    BatchSummarizationComponent,
    LoginComponent,
    EmployeeOverviewComponent,
    EmpAccordianComponent,
    EmpAccordianCardComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    CommonModule,
    ToastrModule.forRoot(),
    FormsModule
  ],
  providers: [
    UploadService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
