/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 - 2021 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, Input, OnInit } from '@angular/core';
import { CmdbMode } from '../../../framework/modes.enum';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ExportdJob } from '../../../settings/models/exportd-job';
import { ExportdJobBaseStepComponent } from '../exportd-job-base-step.component';

@Component({
  selector: 'cmdb-task-scheduling-step',
  templateUrl: './exportd-job-scheduling-step.component.html',
  styleUrls: ['./exportd-job-scheduling-step.component.scss']
})
export class ExportdJobSchedulingStepComponent extends ExportdJobBaseStepComponent implements OnInit {

  @Input()
  set preData(data: ExportdJob) {
    if (data !== undefined && data.scheduling !== undefined) {
      this.eventForm.patchValue(data.scheduling.event);
      this.taskType = data.exportd_type;
    }
  }

  public eventForm: FormGroup;

  /**
   * Type of execution (PULL or PUSH)
   */
  public taskType: string;

  /**
   * Information on the exception rule
   */
  public info: string = 'Excludes jobs that have been executed manually ' +
    'and jobs that are executed automatically after they have been created.';

  constructor(private formBuilder: FormBuilder) {
    super();
    this.eventForm = this.formBuilder.group({
      active: new FormControl(false, Validators.required),
      subset: new FormControl(false, Validators.required),
    });
  }

  public ngOnInit(): void {
    if (this.mode === CmdbMode.Edit) {
      this.eventForm.markAllAsTouched();
    }
  }
}
