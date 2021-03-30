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

import { Component, OnDestroy, OnInit } from '@angular/core';
import { BaseSectionComponent } from '../base-section/base-section.component';
import { TypeService } from '../../../services/type.service';
import { CmdbMode } from '../../../modes.enum';
import { CmdbType } from '../../../models/cmdb-type';
import { ReplaySubject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'cmdb-reference-section',
  templateUrl: './reference-section.component.html',
  styleUrls: ['./reference-section.component.scss']
})
export class ReferenceSectionComponent extends BaseSectionComponent implements OnInit, OnDestroy {

  private subscriber: ReplaySubject<void> = new ReplaySubject<void>();
  public referencedType: CmdbType;

  constructor(private typeService: TypeService) {
    super();
  }

  public ngOnInit(): void {
    if (this.mode === CmdbMode.View) {
      this.typeService.getType(this.section.reference.type_id).pipe(takeUntil(this.subscriber))
        .subscribe((apiResponse: CmdbType) => {
          this.referencedType = apiResponse;
        });
    }
  }

  public get referenceField(): any {
    return this.fields.find(f => f.name === `${this.section.name}-field`);
  }

  public getFieldByName(name: string) {
    const field: any = this.fields[0].references.fields.find(f => f.name === name);
    switch (field.type) {
      case 'ref': {
        field.default = parseInt(field.default, 10);
        field.value = field.default;
        break;
      }
      default: {
        field.default = field.value;
        break;
      }
    }
    return field;
  }

  public getValueByName(name: string) {
    const fieldFound = this.fields[0].references.fields.find(field => field.name === name);
    if (fieldFound === undefined) {
      return {};
    }
    return fieldFound.value;
  }


  public ngOnDestroy(): void {
    this.subscriber.next();
    this.subscriber.complete();
  }


}
