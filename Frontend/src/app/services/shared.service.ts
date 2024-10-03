import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SharedService {

  private dataSource = new BehaviorSubject<any>(null);
  private questionNo = new BehaviorSubject<any>(null);
  employeeData = this.dataSource.asObservable();
  questionNu = this.questionNo.asObservable();

  constructor() { }

  empData(data: any) {
    this.dataSource.next(data);
  }
  queNo(question) {
    this.questionNo.next(question);
  }

}
