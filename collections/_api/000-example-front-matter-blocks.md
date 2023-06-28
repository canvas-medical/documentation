---
title: "Example Front Matter Blocks"
sections:
  - type: "section"
    blocks:
      - type: "path"
        name: "patient"
        path:
          get:
            parameters:
              '0':
                in: query
                name: active
                schema:
                  title: Active
                  type: string
                  description: Whether the patient record is active
                required: 'false'
                description: Whether the patient record is active
              '3':
                schema:
                  description: A portion of the family name of the patient
                  type: string
                  title: Family
                name: family
                in: query
                required: 'false'
                description: A portion of the family name of the patient
              '14':
                schema:
                  title: Pretty
                  description: Ask for a pretty printed response for human convenience
                  type: string
                description: Ask for a pretty printed response for human convenience
                name: _pretty
                in: query
                required: 'false'
              '13':
                in: query
                name: _format
                schema:
                  title: Format
                  description: Override the HTTP content negotiation to specify JSON or XML
                    response format
                  type: string
                description: Override the HTTP content negotiation to specify JSON or XML response
                  format
                required: 'false'
              '9':
                schema:
                  description: A value in a phone contact
                  title: Phone
                  type: string
                required: 'false'
                in: query
                description: A value in a phone contact
                name: phone
              '8':
                name: nickname
                schema:
                  description: Preferred or alternate name
                  type: string
                  title: Nickname
                required: 'false'
                in: query
                description: Preferred or alternate name
              '12':
                name: _sort
                schema:
                  type: string
                  description: 'Order to sort results in (can repeat for inner sort orders)  Allowable
                    Content: Name of a valid search parameter'
                  title: Sort
                required: 'false'
                in: query
                description: 'Order to sort results in (can repeat for inner sort orders)  Allowable
                  Content: Name of a valid search parameter'
              '11':
                description: 'Other resources to include in the search results when they refer
                  to search matches  Allowable Content: SourceType:searchParam(:targetType)'
                in: query
                schema:
                  description: 'Other resources to include in the search results when they refer
                    to search matches  Allowable Content: SourceType:searchParam(:targetType)'
                  title: Revinclude
                  type: string
                name: _revinclude
                required: 'false'
              '1':
                name: birthdate
                required: 'false'
                schema:
                  description: '''The patient''''s date of birth'''
                  title: Birthdate
                  type: string
                in: query
                description: '''The patient''''s date of birth'''
              '7':
                name: name
                schema:
                  type: string
                  title: Name
                  description: A server defined search that may match any of the string fields
                    in the HumanName, including family, give, prefix, suffix, suffix, and/or
                    text
                description: A server defined search that may match any of the string fields
                  in the HumanName, including family, give, prefix, suffix, suffix, and/or text
                in: query
                required: 'false'
              '6':
                schema:
                  type: string
                  description: A patient identifier
                  title: Identifier
                description: A patient identifier
                required: 'false'
                name: identifier
                in: query
              '4':
                schema:
                  description: Gender of the patient
                  title: Gender
                  type: string
                description: Gender of the patient
                required: 'false'
                name: gender
                in: query
              '2':
                schema:
                  description: A value in an email contact
                  type: string
                  title: Email
                in: query
                description: A value in an email contact
                name: email
                required: 'false'
              '10':
                description: Logical id of this artifact
                schema:
                  description: Logical id of this artifact
                  type: string
                  title: Id
                name: _id
                required: 'false'
                in: query
              '5':
                schema:
                  description: A portion of the given name of the patient
                  type: string
                  title: Given
                in: query
                required: 'false'
                description: A portion of the given name of the patient
                name: given
            responses:
              '200':
                content:
                  application/fhir+json:
                    schema:
                      example:
                        entry:
                          '0':
                            resource:
                              telecom:
                                '1':
                                  rank: '1'
                                  value: (03) 5555 6473
                                  system: phone
                                  use: work
                                '3':
                                  system: phone
                                  period:
                                    end: '2014'
                                  use: old
                                  value: (03) 5555 8834
                                '2':
                                  rank: '2'
                                  system: phone
                                  use: mobile
                                  value: (03) 3410 5613
                                '0':
                                  use: home
                              address:
                                '0':
                                  use: home
                                  state: Vic
                                  text: 534 Erewhon St PeasantVille, Rainbow, Vic  3999
                                  line:
                                    '0': 534 Erewhon St
                                  city: PleasantVille
                                  postalCode: '3999'
                                  period:
                                    start: '1974-12-25'
                                  type: both
                                  district: Rainbow
                              identifier:
                                '0':
                                  value: '12345'
                                  period:
                                    start: '2001-05-06'
                                  type:
                                    coding:
                                      '0':
                                        code: MR
                                        system: http://terminology.hl7.org/CodeSystem/v2-0203
                                  assigner:
                                    display: Acme Healthcare
                                  use: usual
                                  system: urn:oid:1.2.36.146.595.217.0.1
                              gender: male
                              contact:
                                '0':
                                  period:
                                    start: '2012'
                                  address:
                                    period:
                                      start: '1974-12-25'
                                    city: PleasantVille
                                    use: home
                                    type: both
                                    postalCode: '3999'
                                    district: Rainbow
                                    state: Vic
                                    line:
                                      '0': 534 Erewhon St
                                  telecom:
                                    '0':
                                      value: +33 (237) 998327
                                      system: phone
                                  relationship:
                                    '0':
                                      coding:
                                        '0':
                                          code: N
                                          system: http://terminology.hl7.org/CodeSystem/v2-0131
                                  name:
                                    _family:
                                      extension:
                                        '0':
                                          valueString: VV
                                          url: http://hl7.org/fhir/StructureDefinition/humanname-own-prefix
                                    family: du MarchÃ©
                                    given:
                                      '0': BÃ©nÃ©dicte
                                  gender: female
                              name:
                                '1':
                                  given:
                                    '0': Jim
                                  use: usual
                                '0':
                                  family: Chalmers
                                  given:
                                    '0': Peter
                                    '1': James
                                  use: official
                                '2':
                                  period:
                                    end: '2002'
                                  given:
                                    '1': James
                                    '0': Peter
                                  family: Windsor
                                  use: maiden
                              text:
                                div: '<div xmlns="http://www.w3.org/1999/xhtml">    <table>     <tbody>      <tr>       <td>Name</td>       <td>Peter
                                  James                <b>Chalmers</b> (&quot;Jim&quot;)             </td>      </tr>      <tr>       <td>Address</td>       <td>534
                                  Erewhon, Pleasantville, Vic, 3999</td>      </tr>      <tr>       <td>Contacts</td>       <td>Home:
                                  unknown. Work: (03) 5555 6473</td>      </tr>      <tr>       <td>Id</td>       <td>MRN:
                                  12345 (Acme Healthcare)</td>      </tr>     </tbody>    </table>   </div>'
                                status: generated
                              active: 'true'
                              meta:
                                tag:
                                  '0':
                                    system: http://terminology.hl7.org/CodeSystem/v3-ActReason
                                    code: HTEST
                                    display: test health data
                              deceasedBoolean: 'false'
                              birthDate: '1974-12-25'
                              managingOrganization:
                                reference: Organization/1
                              _birthDate:
                                extension:
                                  '0':
                                    valueDateTime: '1974-12-25T14:35:45-05:00'
                                    url: http://hl7.org/fhir/StructureDefinition/patient-birthTime
                              resourceType: Patient
                              id: example
                            search:
                              mode: match
                              score: '1'
                            fullUrl: https://example.com/base/Patient/3123
                        link:
                          '0':
                            relation: self
                            url: https://example.com/base/Patient?_count=1
                          '1':
                            url: https://example.com/base/Patient?searchId=ff15fd40-ff71-4b48-b366-09c706bed9d0&page=2
                            relation: next
                        type: searchset
                        meta:
                          tag:
                            '0':
                              code: HTEST
                              display: test health data
                              system: http://terminology.hl7.org/CodeSystem/v3-ActReason
                          lastUpdated: '2014-08-18T01:43:30Z'
                        resourceType: Bundle
                        total: '3'
                        id: bundle-example
                      properties:
                        language:
                          element_property: 'true'
                          pattern: ^[^s]+(s[^s]+)*$
                          title: Language of the resource content
                          type: string
                          description: The base language in which the resource is written.
                        identifier:
                          element_property: 'true'
                          type: Identifier
                          title: Persistent identifier for the bundle
                          description: '''A persistent identifier for the bundle that won''''t
                            change as a bundle is copied from server to server.'''
                        entry:
                          items:
                            type: BundleEntry
                          type: array
                          description: An entry in a bundle resource - will either contain a
                            resource or information about a resource (transactions and history
                            only).
                          element_property: 'true'
                          title: Entry in the bundle - will have a resource or information
                        timestamp:
                          title: When the bundle was assembled
                          format: date-time
                          description: The date/time that the bundle was assembled - i.e. when
                            the resources were placed in the bundle.
                          type: string
                          element_property: 'true'
                        signature:
                          type: Signature
                          element_property: 'true'
                          description: Digital Signature - base64 encoded. XML-DSig or a JWT.
                          title: Digital Signature
                        _language:
                          type: FHIRPrimitiveExtension
                          title: Extension field for ``language``.
                        total:
                          type: integer
                          minimum: '0'
                          title: If search, the total number of matches
                          description: '''If a set of search matches, this is the total number
                            of entries of type ''''match'''' across all pages in the search.  It
                            does not include search.mode = ''''include'''' or ''''outcome''''
                            entries and it does not provide a count of the number of entries
                            in the Bundle.'''
                          element_property: 'true'
                        type:
                          pattern: ^[^s]+(s[^s]+)*$
                          element_required: 'true'
                          description: Indicates the purpose of this bundle - how it is intended
                            to be used.
                          title: document | message | transaction | transaction-response | batch
                            | batch-response | history | searchset | collection
                          type: string
                          element_property: 'true'
                          enum_values:
                            '1': message
                            '0': document
                            '7': searchset
                            '6': history
                            '8': collection
                            '3': transaction-response
                            '2': transaction
                            '5': batch-response
                            '4': batch
                        _type:
                          type: FHIRPrimitiveExtension
                          title: Extension field for ``type``.
                        _implicitRules:
                          title: Extension field for ``implicitRules``.
                          type: FHIRPrimitiveExtension
                        resource_type:
                          const: Bundle
                          default: Bundle
                          type: string
                          title: Resource Type
                        implicitRules:
                          type: string
                          description: A reference to a set of rules that were followed when
                            the resource was constructed, and which must be understood when
                            processing the content. Often, this is a reference to an implementation
                            guide that defines the special rules along with other profiles etc.
                          pattern: S*
                          element_property: 'true'
                          title: A set of rules under which this content was created
                        _total:
                          type: FHIRPrimitiveExtension
                          title: Extension field for ``total``.
                        id:
                          pattern: ^[A-Za-z0-9-.]+$
                          description: The logical id of the resource, as used in the URL for
                            the resource. Once assigned, this value never changes.
                          title: Logical id of this artifact
                          element_property: 'true'
                          maxLength: '64'
                          minLength: '1'
                          type: string
                        link:
                          type: array
                          description: A series of links that provide context to this bundle.
                          items:
                            type: BundleLink
                          element_property: 'true'
                          title: Links related to this Bundle
                        fhir_comments:
                          anyOf:
                            '1':
                              items:
                                type: string
                              type: array
                            '0':
                              type: string
                          title: Fhir Comments
                          element_property: 'false'
                        meta:
                          element_property: 'true'
                          description: The metadata about the resource. This is content that
                            is maintained by the infrastructure. Changes to the content might
                            not always be associated with version changes to the resource.
                          type: Meta
                          title: Metadata about the resource
                        _timestamp:
                          title: Extension field for ``timestamp``.
                          type: FHIRPrimitiveExtension
                      title: Bundle
                      additionalProperties: 'false'
                      type: object
                      description: '''Disclaimer: Any field name ends with ``__ext`` doesn''''t
                        part of Resource StructureDefinition, instead used to enable Extensibility
                        feature for FHIR Primitive Data Types.  Contains a collection of resources.
                        A container for a collection of resources.'''
                description: Successful Patient search-type
              '400':
                content:
                  application/fhir+json:
                    type: object
                    properties:
                      fhir_comments:
                        anyOf:
                          '1':
                            items:
                              type: string
                            type: array
                          '0':
                            type: string
                        element_property: 'false'
                        title: Fhir Comments
                      contained:
                        element_property: 'true'
                        items:
                          type: Resource
                        description: These resources do not have an independent existence apart
                          from the resource that contains them - they cannot be identified independently,
                          and nor can they have their own independent transaction scope.
                        type: array
                        title: Contained, inline Resources
                      issue:
                        element_property: 'true'
                        title: A single issue associated with the action
                        type: array
                        items:
                          type: OperationOutcomeIssue
                        description: An error, warning, or information message that results
                          from a system action.
                      id:
                        maxLength: '64'
                        minLength: '1'
                        type: string
                        description: The logical id of the resource, as used in the URL for
                          the resource. Once assigned, this value never changes.
                        title: Logical id of this artifact
                        element_property: 'true'
                        pattern: ^[A-Za-z0-9-.]+$
                      _implicitRules:
                        title: Extension field for ``implicitRules``.
                        type: FHIRPrimitiveExtension
                      language:
                        pattern: ^[^s]+(s[^s]+)*$
                        title: Language of the resource content
                        element_property: 'true'
                        description: The base language in which the resource is written.
                        type: string
                      modifierExtension:
                        description: '''May be used to represent additional information that
                          is not part of the basic definition of the resource and that modifies
                          the understanding of the element that contains it and/or the understanding
                          of the containing element''''s descendants. Usually modifier elements
                          provide negation or qualification. To make the use of extensions safe
                          and manageable, there is a strict set of governance applied to the
                          definition and use of extensions. Though any implementer is allowed
                          to define an extension, there is a set of requirements that SHALL
                          be met as part of the definition of the extension. Applications processing
                          a resource are required to check for modifier extensions.  Modifier
                          extensions SHALL NOT change the meaning of any elements on Resource
                          or DomainResource (including cannot change the meaning of modifierExtension
                          itself).'''
                        title: Extensions that cannot be ignored
                        type: array
                        element_property: 'true'
                        items:
                          type: Extension
                      _language:
                        type: FHIRPrimitiveExtension
                        title: Extension field for ``language``.
                      implicitRules:
                        title: A set of rules under which this content was created
                        element_property: 'true'
                        description: A reference to a set of rules that were followed when the
                          resource was constructed, and which must be understood when processing
                          the content. Often, this is a reference to an implementation guide
                          that defines the special rules along with other profiles etc.
                        type: string
                        pattern: S*
                      extension:
                        title: Additional content defined by implementations
                        items:
                          type: Extension
                        description: May be used to represent additional information that is
                          not part of the basic definition of the resource. To make the use
                          of extensions safe and manageable, there is a strict set of governance  applied
                          to the definition and use of extensions. Though any implementer can
                          define an extension, there is a set of requirements that SHALL be
                          met as part of the definition of the extension.
                        type: array
                        element_property: 'true'
                      meta:
                        element_property: 'true'
                        type: Meta
                        title: Metadata about the resource
                        description: The metadata about the resource. This is content that is
                          maintained by the infrastructure. Changes to the content might not
                          always be associated with version changes to the resource.
                      resource_type:
                        const: OperationOutcome
                        type: string
                        title: Resource Type
                        default: OperationOutcome
                      text:
                        element_property: 'true'
                        title: Text summary of the resource, for human interpretation
                        type: Narrative
                        description: A human-readable narrative that contains a summary of the
                          resource and can be used to represent the content of the resource
                          to a human. The narrative need not encode all the structured data,
                          but is required to contain sufficient detail to make it "clinically
                          safe" for a human to just read the narrative. Resource definitions
                          may define what content should be represented in the narrative to
                          ensure clinical safety.
                    required:
                      '0': issue
                    example:
                      issue:
                        '0':
                          code: invalid
                          severity: error
                          details:
                            text: Bad Request
                      id: '101'
                      resourceType: OperationOutcome
                    description: '''Disclaimer: Any field name ends with ``__ext`` doesn''''t
                      part of Resource StructureDefinition, instead used to enable Extensibility
                      feature for FHIR Primitive Data Types.  Information about the success/failure
                      of an action. A collection of error, warning, or information messages
                      that result from a system action.'''
                    additionalProperties: 'false'
                    title: OperationOutcome 400
                description: Patient search-type request could not be parsed or failed basic
                  FHIR validation rules.
              '401':
                content:
                  application/fhir+json:
                    example:
                      issue:
                        '0':
                          details:
                            text: Authentication failed
                          code: unknown
                          severity: error
                      id: '101'
                      resourceType: OperationOutcome
                    properties:
                      meta:
                        title: Metadata about the resource
                        description: The metadata about the resource. This is content that is
                          maintained by the infrastructure. Changes to the content might not
                          always be associated with version changes to the resource.
                        type: Meta
                        element_property: 'true'
                      issue:
                        items:
                          type: OperationOutcomeIssue
                        element_property: 'true'
                        type: array
                        title: A single issue associated with the action
                        description: An error, warning, or information message that results
                          from a system action.
                      modifierExtension:
                        type: array
                        element_property: 'true'
                        title: Extensions that cannot be ignored
                        description: '''May be used to represent additional information that
                          is not part of the basic definition of the resource and that modifies
                          the understanding of the element that contains it and/or the understanding
                          of the containing element''''s descendants. Usually modifier elements
                          provide negation or qualification. To make the use of extensions safe
                          and manageable, there is a strict set of governance applied to the
                          definition and use of extensions. Though any implementer is allowed
                          to define an extension, there is a set of requirements that SHALL
                          be met as part of the definition of the extension. Applications processing
                          a resource are required to check for modifier extensions.  Modifier
                          extensions SHALL NOT change the meaning of any elements on Resource
                          or DomainResource (including cannot change the meaning of modifierExtension
                          itself).'''
                        items:
                          type: Extension
                      _implicitRules:
                        type: FHIRPrimitiveExtension
                        title: Extension field for ``implicitRules``.
                      id:
                        element_property: 'true'
                        description: The logical id of the resource, as used in the URL for
                          the resource. Once assigned, this value never changes.
                        type: string
                        maxLength: '64'
                        title: Logical id of this artifact
                        pattern: ^[A-Za-z0-9-.]+$
                        minLength: '1'
                      fhir_comments:
                        anyOf:
                          '1':
                            items:
                              type: string
                            type: array
                          '0':
                            type: string
                        element_property: 'false'
                        title: Fhir Comments
                      resource_type:
                        type: string
                        default: OperationOutcome
                        title: Resource Type
                        const: OperationOutcome
                      text:
                        title: Text summary of the resource, for human interpretation
                        description: A human-readable narrative that contains a summary of the
                          resource and can be used to represent the content of the resource
                          to a human. The narrative need not encode all the structured data,
                          but is required to contain sufficient detail to make it "clinically
                          safe" for a human to just read the narrative. Resource definitions
                          may define what content should be represented in the narrative to
                          ensure clinical safety.
                        type: Narrative
                        element_property: 'true'
                      implicitRules:
                        element_property: 'true'
                        description: A reference to a set of rules that were followed when the
                          resource was constructed, and which must be understood when processing
                          the content. Often, this is a reference to an implementation guide
                          that defines the special rules along with other profiles etc.
                        type: string
                        pattern: S*
                        title: A set of rules under which this content was created
                      language:
                        title: Language of the resource content
                        type: string
                        pattern: ^[^s]+(s[^s]+)*$
                        description: The base language in which the resource is written.
                        element_property: 'true'
                      extension:
                        items:
                          type: Extension
                        type: array
                        element_property: 'true'
                        description: May be used to represent additional information that is
                          not part of the basic definition of the resource. To make the use
                          of extensions safe and manageable, there is a strict set of governance  applied
                          to the definition and use of extensions. Though any implementer can
                          define an extension, there is a set of requirements that SHALL be
                          met as part of the definition of the extension.
                        title: Additional content defined by implementations
                      contained:
                        description: These resources do not have an independent existence apart
                          from the resource that contains them - they cannot be identified independently,
                          and nor can they have their own independent transaction scope.
                        items:
                          type: Resource
                        type: array
                        title: Contained, inline Resources
                        element_property: 'true'
                      _language:
                        type: FHIRPrimitiveExtension
                        title: Extension field for ``language``.
                    description: '''Disclaimer: Any field name ends with ``__ext`` doesn''''t
                      part of Resource StructureDefinition, instead used to enable Extensibility
                      feature for FHIR Primitive Data Types.  Information about the success/failure
                      of an action. A collection of error, warning, or information messages
                      that result from a system action.'''
                    type: object
                    required:
                      '0': issue
                    additionalProperties: 'false'
                    title: OperationOutcome 401
                description: Authentication is required for the Patient search-type interaction
                  that was attempted.
              '500':
                content:
                  application/fhir+json:
                    properties:
                      extension:
                        items:
                          type: Extension
                        element_property: 'true'
                        type: array
                        title: Additional content defined by implementations
                        description: May be used to represent additional information that is
                          not part of the basic definition of the resource. To make the use
                          of extensions safe and manageable, there is a strict set of governance  applied
                          to the definition and use of extensions. Though any implementer can
                          define an extension, there is a set of requirements that SHALL be
                          met as part of the definition of the extension.
                      contained:
                        type: array
                        description: These resources do not have an independent existence apart
                          from the resource that contains them - they cannot be identified independently,
                          and nor can they have their own independent transaction scope.
                        title: Contained, inline Resources
                        items:
                          type: Resource
                        element_property: 'true'
                      fhir_comments:
                        anyOf:
                          '1':
                            type: array
                            items:
                              type: string
                          '0':
                            type: string
                        title: Fhir Comments
                        element_property: 'false'
                      meta:
                        title: Metadata about the resource
                        type: Meta
                        description: The metadata about the resource. This is content that is
                          maintained by the infrastructure. Changes to the content might not
                          always be associated with version changes to the resource.
                        element_property: 'true'
                      implicitRules:
                        title: A set of rules under which this content was created
                        element_property: 'true'
                        description: A reference to a set of rules that were followed when the
                          resource was constructed, and which must be understood when processing
                          the content. Often, this is a reference to an implementation guide
                          that defines the special rules along with other profiles etc.
                        type: string
                        pattern: S*
                      resource_type:
                        const: OperationOutcome
                        title: Resource Type
                        default: OperationOutcome
                        type: string
                      issue:
                        element_property: 'true'
                        title: A single issue associated with the action
                        type: array
                        description: An error, warning, or information message that results
                          from a system action.
                        items:
                          type: OperationOutcomeIssue
                      _language:
                        title: Extension field for ``language``.
                        type: FHIRPrimitiveExtension
                      text:
                        description: A human-readable narrative that contains a summary of the
                          resource and can be used to represent the content of the resource
                          to a human. The narrative need not encode all the structured data,
                          but is required to contain sufficient detail to make it "clinically
                          safe" for a human to just read the narrative. Resource definitions
                          may define what content should be represented in the narrative to
                          ensure clinical safety.
                        element_property: 'true'
                        type: Narrative
                        title: Text summary of the resource, for human interpretation
                      language:
                        title: Language of the resource content
                        type: string
                        description: The base language in which the resource is written.
                        element_property: 'true'
                        pattern: ^[^s]+(s[^s]+)*$
                      id:
                        type: string
                        title: Logical id of this artifact
                        element_property: 'true'
                        maxLength: '64'
                        pattern: ^[A-Za-z0-9-.]+$
                        description: The logical id of the resource, as used in the URL for
                          the resource. Once assigned, this value never changes.
                        minLength: '1'
                      modifierExtension:
                        description: '''May be used to represent additional information that
                          is not part of the basic definition of the resource and that modifies
                          the understanding of the element that contains it and/or the understanding
                          of the containing element''''s descendants. Usually modifier elements
                          provide negation or qualification. To make the use of extensions safe
                          and manageable, there is a strict set of governance applied to the
                          definition and use of extensions. Though any implementer is allowed
                          to define an extension, there is a set of requirements that SHALL
                          be met as part of the definition of the extension. Applications processing
                          a resource are required to check for modifier extensions.  Modifier
                          extensions SHALL NOT change the meaning of any elements on Resource
                          or DomainResource (including cannot change the meaning of modifierExtension
                          itself).'''
                        type: array
                        title: Extensions that cannot be ignored
                        element_property: 'true'
                        items:
                          type: Extension
                      _implicitRules:
                        type: FHIRPrimitiveExtension
                        title: Extension field for ``implicitRules``.
                    title: OperationOutcome 500
                    description: '''Disclaimer: Any field name ends with ``__ext`` doesn''''t
                      part of Resource StructureDefinition, instead used to enable Extensibility
                      feature for FHIR Primitive Data Types.  Information about the success/failure
                      of an action. A collection of error, warning, or information messages
                      that result from a system action.'''
                    example:
                      issue:
                        '0':
                          details:
                            text: Internal Server Error
                          severity: error
                          code: exception
                      id: '101'
                      resourceType: OperationOutcome
                    additionalProperties: 'false'
                    required:
                      '0': issue
                    type: object
                description: The server has encountered a situation it does not know how to
                  handle.
              '403':
                content:
                  application/fhir+json:
                    properties:
                      issue:
                        items:
                          type: OperationOutcomeIssue
                        description: An error, warning, or information message that results
                          from a system action.
                        title: A single issue associated with the action
                        type: array
                        element_property: 'true'
                      language:
                        title: Language of the resource content
                        type: string
                        element_property: 'true'
                        description: The base language in which the resource is written.
                        pattern: ^[^s]+(s[^s]+)*$
                      id:
                        description: The logical id of the resource, as used in the URL for
                          the resource. Once assigned, this value never changes.
                        type: string
                        element_property: 'true'
                        pattern: ^[A-Za-z0-9-.]+$
                        minLength: '1'
                        maxLength: '64'
                        title: Logical id of this artifact
                      extension:
                        element_property: 'true'
                        items:
                          type: Extension
                        description: May be used to represent additional information that is
                          not part of the basic definition of the resource. To make the use
                          of extensions safe and manageable, there is a strict set of governance  applied
                          to the definition and use of extensions. Though any implementer can
                          define an extension, there is a set of requirements that SHALL be
                          met as part of the definition of the extension.
                        type: array
                        title: Additional content defined by implementations
                      implicitRules:
                        type: string
                        pattern: S*
                        description: A reference to a set of rules that were followed when the
                          resource was constructed, and which must be understood when processing
                          the content. Often, this is a reference to an implementation guide
                          that defines the special rules along with other profiles etc.
                        title: A set of rules under which this content was created
                        element_property: 'true'
                      fhir_comments:
                        title: Fhir Comments
                        anyOf:
                          '1':
                            type: array
                            items:
                              type: string
                          '0':
                            type: string
                        element_property: 'false'
                      contained:
                        element_property: 'true'
                        items:
                          type: Resource
                        title: Contained, inline Resources
                        description: These resources do not have an independent existence apart
                          from the resource that contains them - they cannot be identified independently,
                          and nor can they have their own independent transaction scope.
                        type: array
                      modifierExtension:
                        items:
                          type: Extension
                        title: Extensions that cannot be ignored
                        type: array
                        element_property: 'true'
                        description: '''May be used to represent additional information that
                          is not part of the basic definition of the resource and that modifies
                          the understanding of the element that contains it and/or the understanding
                          of the containing element''''s descendants. Usually modifier elements
                          provide negation or qualification. To make the use of extensions safe
                          and manageable, there is a strict set of governance applied to the
                          definition and use of extensions. Though any implementer is allowed
                          to define an extension, there is a set of requirements that SHALL
                          be met as part of the definition of the extension. Applications processing
                          a resource are required to check for modifier extensions.  Modifier
                          extensions SHALL NOT change the meaning of any elements on Resource
                          or DomainResource (including cannot change the meaning of modifierExtension
                          itself).'''
                      text:
                        element_property: 'true'
                        title: Text summary of the resource, for human interpretation
                        description: A human-readable narrative that contains a summary of the
                          resource and can be used to represent the content of the resource
                          to a human. The narrative need not encode all the structured data,
                          but is required to contain sufficient detail to make it "clinically
                          safe" for a human to just read the narrative. Resource definitions
                          may define what content should be represented in the narrative to
                          ensure clinical safety.
                        type: Narrative
                      meta:
                        type: Meta
                        description: The metadata about the resource. This is content that is
                          maintained by the infrastructure. Changes to the content might not
                          always be associated with version changes to the resource.
                        element_property: 'true'
                        title: Metadata about the resource
                      _implicitRules:
                        type: FHIRPrimitiveExtension
                        title: Extension field for ``implicitRules``.
                      resource_type:
                        type: string
                        title: Resource Type
                        default: OperationOutcome
                        const: OperationOutcome
                      _language:
                        type: FHIRPrimitiveExtension
                        title: Extension field for ``language``.
                    title: OperationOutcome 403
                    description: '''Disclaimer: Any field name ends with ``__ext`` doesn''''t
                      part of Resource StructureDefinition, instead used to enable Extensibility
                      feature for FHIR Primitive Data Types.  Information about the success/failure
                      of an action. A collection of error, warning, or information messages
                      that result from a system action.'''
                    additionalProperties: 'false'
                    type: object
                    example:
                      issue:
                        '0':
                          severity: error
                          details:
                            text: Authorization failed
                          code: forbidden
                      id: '101'
                      resourceType: OperationOutcome
                    required:
                      '0': issue
                description: Authorization is required for the Patient search-type interaction
                  that was attempted.
            summary: Patient search-type
            description: The Patient search-type interaction searches a set of resources based
              on some filter criteria.
            tags:
              '0': Type:Patient
            operationId: fhirstarter|type|search|get|Patient
          post:
            summary: Patient create
            responses:
              '500':
                content:
                  application/fhir+json:
                    properties:
                      issue:
                        description: An error, warning, or information message that results
                          from a system action.
                        title: A single issue associated with the action
                        items:
                          type: OperationOutcomeIssue
                        type: array
                        element_property: 'true'
                      fhir_comments:
                        element_property: 'false'
                        anyOf:
                          '1':
                            items:
                              type: string
                            type: array
                          '0':
                            type: string
                        title: Fhir Comments
                      modifierExtension:
                        type: array
                        element_property: 'true'
                        title: Extensions that cannot be ignored
                        items:
                          type: Extension
                        description: '''May be used to represent additional information that
                          is not part of the basic definition of the resource and that modifies
                          the understanding of the element that contains it and/or the understanding
                          of the containing element''''s descendants. Usually modifier elements
                          provide negation or qualification. To make the use of extensions safe
                          and manageable, there is a strict set of governance applied to the
                          definition and use of extensions. Though any implementer is allowed
                          to define an extension, there is a set of requirements that SHALL
                          be met as part of the definition of the extension. Applications processing
                          a resource are required to check for modifier extensions.  Modifier
                          extensions SHALL NOT change the meaning of any elements on Resource
                          or DomainResource (including cannot change the meaning of modifierExtension
                          itself).'''
                      id:
                        maxLength: '64'
                        minLength: '1'
                        element_property: 'true'
                        description: The logical id of the resource, as used in the URL for
                          the resource. Once assigned, this value never changes.
                        title: Logical id of this artifact
                        type: string
                        pattern: ^[A-Za-z0-9-.]+$
                      contained:
                        type: array
                        items:
                          type: Resource
                        title: Contained, inline Resources
                        description: These resources do not have an independent existence apart
                          from the resource that contains them - they cannot be identified independently,
                          and nor can they have their own independent transaction scope.
                        element_property: 'true'
                      extension:
                        items:
                          type: Extension
                        type: array
                        element_property: 'true'
                        description: May be used to represent additional information that is
                          not part of the basic definition of the resource. To make the use
                          of extensions safe and manageable, there is a strict set of governance  applied
                          to the definition and use of extensions. Though any implementer can
                          define an extension, there is a set of requirements that SHALL be
                          met as part of the definition of the extension.
                        title: Additional content defined by implementations
                      implicitRules:
                        type: string
                        title: A set of rules under which this content was created
                        element_property: 'true'
                        pattern: S*
                        description: A reference to a set of rules that were followed when the
                          resource was constructed, and which must be understood when processing
                          the content. Often, this is a reference to an implementation guide
                          that defines the special rules along with other profiles etc.
                      meta:
                        description: The metadata about the resource. This is content that is
                          maintained by the infrastructure. Changes to the content might not
                          always be associated with version changes to the resource.
                        element_property: 'true'
                        title: Metadata about the resource
                        type: Meta
                      language:
                        element_property: 'true'
                        title: Language of the resource content
                        type: string
                        pattern: ^[^s]+(s[^s]+)*$
                        description: The base language in which the resource is written.
                      _implicitRules:
                        type: FHIRPrimitiveExtension
                        title: Extension field for ``implicitRules``.
                      text:
                        type: Narrative
                        description: A human-readable narrative that contains a summary of the
                          resource and can be used to represent the content of the resource
                          to a human. The narrative need not encode all the structured data,
                          but is required to contain sufficient detail to make it "clinically
                          safe" for a human to just read the narrative. Resource definitions
                          may define what content should be represented in the narrative to
                          ensure clinical safety.
                        title: Text summary of the resource, for human interpretation
                        element_property: 'true'
                      resource_type:
                        type: string
                        default: OperationOutcome
                        title: Resource Type
                        const: OperationOutcome
                      _language:
                        type: FHIRPrimitiveExtension
                        title: Extension field for ``language``.
                    example:
                      id: '101'
                      issue:
                        '0':
                          details:
                            text: Internal Server Error
                          code: exception
                          severity: error
                      resourceType: OperationOutcome
                    description: '''Disclaimer: Any field name ends with ``__ext`` doesn''''t
                      part of Resource StructureDefinition, instead used to enable Extensibility
                      feature for FHIR Primitive Data Types.  Information about the success/failure
                      of an action. A collection of error, warning, or information messages
                      that result from a system action.'''
                    additionalProperties: 'false'
                    title: OperationOutcome 500
                    type: object
                    required:
                      '0': issue
                description: The server has encountered a situation it does not know how to
                  handle.
              '403':
                content:
                  application/fhir+json:
                    required:
                      '0': issue
                    properties:
                      contained:
                        title: Contained, inline Resources
                        items:
                          type: Resource
                        type: array
                        element_property: 'true'
                        description: These resources do not have an independent existence apart
                          from the resource that contains them - they cannot be identified independently,
                          and nor can they have their own independent transaction scope.
                      modifierExtension:
                        element_property: 'true'
                        type: array
                        description: '''May be used to represent additional information that
                          is not part of the basic definition of the resource and that modifies
                          the understanding of the element that contains it and/or the understanding
                          of the containing element''''s descendants. Usually modifier elements
                          provide negation or qualification. To make the use of extensions safe
                          and manageable, there is a strict set of governance applied to the
                          definition and use of extensions. Though any implementer is allowed
                          to define an extension, there is a set of requirements that SHALL
                          be met as part of the definition of the extension. Applications processing
                          a resource are required to check for modifier extensions.  Modifier
                          extensions SHALL NOT change the meaning of any elements on Resource
                          or DomainResource (including cannot change the meaning of modifierExtension
                          itself).'''
                        items:
                          type: Extension
                        title: Extensions that cannot be ignored
                      id:
                        description: The logical id of the resource, as used in the URL for
                          the resource. Once assigned, this value never changes.
                        pattern: ^[A-Za-z0-9-.]+$
                        element_property: 'true'
                        maxLength: '64'
                        title: Logical id of this artifact
                        type: string
                        minLength: '1'
                      issue:
                        type: array
                        title: A single issue associated with the action
                        element_property: 'true'
                        description: An error, warning, or information message that results
                          from a system action.
                        items:
                          type: OperationOutcomeIssue
                      fhir_comments:
                        anyOf:
                          '1':
                            type: array
                            items:
                              type: string
                          '0':
                            type: string
                        title: Fhir Comments
                        element_property: 'false'
                      language:
                        element_property: 'true'
                        type: string
                        description: The base language in which the resource is written.
                        title: Language of the resource content
                        pattern: ^[^s]+(s[^s]+)*$
                      meta:
                        description: The metadata about the resource. This is content that is
                          maintained by the infrastructure. Changes to the content might not
                          always be associated with version changes to the resource.
                        element_property: 'true'
                        title: Metadata about the resource
                        type: Meta
                      extension:
                        items:
                          type: Extension
                        title: Additional content defined by implementations
                        description: May be used to represent additional information that is
                          not part of the basic definition of the resource. To make the use
                          of extensions safe and manageable, there is a strict set of governance  applied
                          to the definition and use of extensions. Though any implementer can
                          define an extension, there is a set of requirements that SHALL be
                          met as part of the definition of the extension.
                        element_property: 'true'
                        type: array
                      _implicitRules:
                        type: FHIRPrimitiveExtension
                        title: Extension field for ``implicitRules``.
                      _language:
                        title: Extension field for ``language``.
                        type: FHIRPrimitiveExtension
                      implicitRules:
                        type: string
                        description: A reference to a set of rules that were followed when the
                          resource was constructed, and which must be understood when processing
                          the content. Often, this is a reference to an implementation guide
                          that defines the special rules along with other profiles etc.
                        element_property: 'true'
                        pattern: S*
                        title: A set of rules under which this content was created
                      text:
                        type: Narrative
                        element_property: 'true'
                        description: A human-readable narrative that contains a summary of the
                          resource and can be used to represent the content of the resource
                          to a human. The narrative need not encode all the structured data,
                          but is required to contain sufficient detail to make it "clinically
                          safe" for a human to just read the narrative. Resource definitions
                          may define what content should be represented in the narrative to
                          ensure clinical safety.
                        title: Text summary of the resource, for human interpretation
                      resource_type:
                        default: OperationOutcome
                        type: string
                        title: Resource Type
                        const: OperationOutcome
                    additionalProperties: 'false'
                    example:
                      issue:
                        '0':
                          details:
                            text: Authorization failed
                          code: forbidden
                          severity: error
                      id: '101'
                      resourceType: OperationOutcome
                    description: '''Disclaimer: Any field name ends with ``__ext`` doesn''''t
                      part of Resource StructureDefinition, instead used to enable Extensibility
                      feature for FHIR Primitive Data Types.  Information about the success/failure
                      of an action. A collection of error, warning, or information messages
                      that result from a system action.'''
                    title: OperationOutcome 403
                    type: object
                description: Authorization is required for the Patient create interaction that
                  was attempted.
              '422':
                content:
                  application/fhir+json:
                    properties:
                      modifierExtension:
                        title: Extensions that cannot be ignored
                        items:
                          type: Extension
                        element_property: 'true'
                        description: '''May be used to represent additional information that
                          is not part of the basic definition of the resource and that modifies
                          the understanding of the element that contains it and/or the understanding
                          of the containing element''''s descendants. Usually modifier elements
                          provide negation or qualification. To make the use of extensions safe
                          and manageable, there is a strict set of governance applied to the
                          definition and use of extensions. Though any implementer is allowed
                          to define an extension, there is a set of requirements that SHALL
                          be met as part of the definition of the extension. Applications processing
                          a resource are required to check for modifier extensions.  Modifier
                          extensions SHALL NOT change the meaning of any elements on Resource
                          or DomainResource (including cannot change the meaning of modifierExtension
                          itself).'''
                        type: array
                      id:
                        maxLength: '64'
                        minLength: '1'
                        description: The logical id of the resource, as used in the URL for
                          the resource. Once assigned, this value never changes.
                        title: Logical id of this artifact
                        element_property: 'true'
                        pattern: ^[A-Za-z0-9-.]+$
                        type: string
                      contained:
                        element_property: 'true'
                        description: These resources do not have an independent existence apart
                          from the resource that contains them - they cannot be identified independently,
                          and nor can they have their own independent transaction scope.
                        title: Contained, inline Resources
                        items:
                          type: Resource
                        type: array
                      extension:
                        title: Additional content defined by implementations
                        description: May be used to represent additional information that is
                          not part of the basic definition of the resource. To make the use
                          of extensions safe and manageable, there is a strict set of governance  applied
                          to the definition and use of extensions. Though any implementer can
                          define an extension, there is a set of requirements that SHALL be
                          met as part of the definition of the extension.
                        items:
                          type: Extension
                        element_property: 'true'
                        type: array
                      fhir_comments:
                        anyOf:
                          '1':
                            type: array
                            items:
                              type: string
                          '0':
                            type: string
                        title: Fhir Comments
                        element_property: 'false'
                      language:
                        title: Language of the resource content
                        element_property: 'true'
                        pattern: ^[^s]+(s[^s]+)*$
                        type: string
                        description: The base language in which the resource is written.
                      meta:
                        description: The metadata about the resource. This is content that is
                          maintained by the infrastructure. Changes to the content might not
                          always be associated with version changes to the resource.
                        title: Metadata about the resource
                        type: Meta
                        element_property: 'true'
                      resource_type:
                        const: OperationOutcome
                        type: string
                        title: Resource Type
                        default: OperationOutcome
                      implicitRules:
                        type: string
                        description: A reference to a set of rules that were followed when the
                          resource was constructed, and which must be understood when processing
                          the content. Often, this is a reference to an implementation guide
                          that defines the special rules along with other profiles etc.
                        title: A set of rules under which this content was created
                        pattern: S*
                        element_property: 'true'
                      issue:
                        type: array
                        description: An error, warning, or information message that results
                          from a system action.
                        items:
                          type: OperationOutcomeIssue
                        element_property: 'true'
                        title: A single issue associated with the action
                      _language:
                        type: FHIRPrimitiveExtension
                        title: Extension field for ``language``.
                      text:
                        type: Narrative
                        element_property: 'true'
                        description: A human-readable narrative that contains a summary of the
                          resource and can be used to represent the content of the resource
                          to a human. The narrative need not encode all the structured data,
                          but is required to contain sufficient detail to make it "clinically
                          safe" for a human to just read the narrative. Resource definitions
                          may define what content should be represented in the narrative to
                          ensure clinical safety.
                        title: Text summary of the resource, for human interpretation
                      _implicitRules:
                        type: FHIRPrimitiveExtension
                        title: Extension field for ``implicitRules``.
                    example:
                      id: '101'
                      resourceType: OperationOutcome
                      issue:
                        '0':
                          details:
                            text: Unprocessable Entity
                          code: processing
                          severity: error
                    description: '''Disclaimer: Any field name ends with ``__ext`` doesn''''t
                      part of Resource StructureDefinition, instead used to enable Extensibility
                      feature for FHIR Primitive Data Types.  Information about the success/failure
                      of an action. A collection of error, warning, or information messages
                      that result from a system action.'''
                    required:
                      '0': issue
                    additionalProperties: 'false'
                    title: OperationOutcome 422
                    type: object
                description: The proposed Patient resource violated applicable FHIR profiles
                  or server business rules.
              '401':
                content:
                  application/fhir+json:
                    properties:
                      _implicitRules:
                        type: FHIRPrimitiveExtension
                        title: Extension field for ``implicitRules``.
                      id:
                        element_property: 'true'
                        description: The logical id of the resource, as used in the URL for
                          the resource. Once assigned, this value never changes.
                        maxLength: '64'
                        minLength: '1'
                        title: Logical id of this artifact
                        pattern: ^[A-Za-z0-9-.]+$
                        type: string
                      resource_type:
                        default: OperationOutcome
                        title: Resource Type
                        const: OperationOutcome
                        type: string
                      language:
                        element_property: 'true'
                        pattern: ^[^s]+(s[^s]+)*$
                        type: string
                        description: The base language in which the resource is written.
                        title: Language of the resource content
                      issue:
                        type: array
                        items:
                          type: OperationOutcomeIssue
                        description: An error, warning, or information message that results
                          from a system action.
                        title: A single issue associated with the action
                        element_property: 'true'
                      fhir_comments:
                        anyOf:
                          '1':
                            items:
                              type: string
                            type: array
                          '0':
                            type: string
                        title: Fhir Comments
                        element_property: 'false'
                      modifierExtension:
                        title: Extensions that cannot be ignored
                        description: '''May be used to represent additional information that
                          is not part of the basic definition of the resource and that modifies
                          the understanding of the element that contains it and/or the understanding
                          of the containing element''''s descendants. Usually modifier elements
                          provide negation or qualification. To make the use of extensions safe
                          and manageable, there is a strict set of governance applied to the
                          definition and use of extensions. Though any implementer is allowed
                          to define an extension, there is a set of requirements that SHALL
                          be met as part of the definition of the extension. Applications processing
                          a resource are required to check for modifier extensions.  Modifier
                          extensions SHALL NOT change the meaning of any elements on Resource
                          or DomainResource (including cannot change the meaning of modifierExtension
                          itself).'''
                        element_property: 'true'
                        type: array
                        items:
                          type: Extension
                      text:
                        type: Narrative
                        description: A human-readable narrative that contains a summary of the
                          resource and can be used to represent the content of the resource
                          to a human. The narrative need not encode all the structured data,
                          but is required to contain sufficient detail to make it "clinically
                          safe" for a human to just read the narrative. Resource definitions
                          may define what content should be represented in the narrative to
                          ensure clinical safety.
                        title: Text summary of the resource, for human interpretation
                        element_property: 'true'
                      contained:
                        element_property: 'true'
                        description: These resources do not have an independent existence apart
                          from the resource that contains them - they cannot be identified independently,
                          and nor can they have their own independent transaction scope.
                        title: Contained, inline Resources
                        items:
                          type: Resource
                        type: array
                      meta:
                        element_property: 'true'
                        description: The metadata about the resource. This is content that is
                          maintained by the infrastructure. Changes to the content might not
                          always be associated with version changes to the resource.
                        title: Metadata about the resource
                        type: Meta
                      _language:
                        title: Extension field for ``language``.
                        type: FHIRPrimitiveExtension
                      implicitRules:
                        element_property: 'true'
                        pattern: S*
                        description: A reference to a set of rules that were followed when the
                          resource was constructed, and which must be understood when processing
                          the content. Often, this is a reference to an implementation guide
                          that defines the special rules along with other profiles etc.
                        type: string
                        title: A set of rules under which this content was created
                      extension:
                        title: Additional content defined by implementations
                        items:
                          type: Extension
                        description: May be used to represent additional information that is
                          not part of the basic definition of the resource. To make the use
                          of extensions safe and manageable, there is a strict set of governance  applied
                          to the definition and use of extensions. Though any implementer can
                          define an extension, there is a set of requirements that SHALL be
                          met as part of the definition of the extension.
                        type: array
                        element_property: 'true'
                    additionalProperties: 'false'
                    example:
                      id: '101'
                      issue:
                        '0':
                          code: unknown
                          details:
                            text: Authentication failed
                          severity: error
                      resourceType: OperationOutcome
                    type: object
                    description: '''Disclaimer: Any field name ends with ``__ext`` doesn''''t
                      part of Resource StructureDefinition, instead used to enable Extensibility
                      feature for FHIR Primitive Data Types.  Information about the success/failure
                      of an action. A collection of error, warning, or information messages
                      that result from a system action.'''
                    title: OperationOutcome 401
                    required:
                      '0': issue
                description: Authentication is required for the Patient create interaction that
                  was attempted.
              '400':
                content:
                  application/fhir+json:
                    properties:
                      _language:
                        type: FHIRPrimitiveExtension
                        title: Extension field for ``language``.
                      meta:
                        title: Metadata about the resource
                        element_property: 'true'
                        description: The metadata about the resource. This is content that is
                          maintained by the infrastructure. Changes to the content might not
                          always be associated with version changes to the resource.
                        type: Meta
                      id:
                        type: string
                        title: Logical id of this artifact
                        minLength: '1'
                        element_property: 'true'
                        pattern: ^[A-Za-z0-9-.]+$
                        description: The logical id of the resource, as used in the URL for
                          the resource. Once assigned, this value never changes.
                        maxLength: '64'
                      fhir_comments:
                        element_property: 'false'
                        title: Fhir Comments
                        anyOf:
                          '1':
                            type: array
                            items:
                              type: string
                          '0':
                            type: string
                      extension:
                        description: May be used to represent additional information that is
                          not part of the basic definition of the resource. To make the use
                          of extensions safe and manageable, there is a strict set of governance  applied
                          to the definition and use of extensions. Though any implementer can
                          define an extension, there is a set of requirements that SHALL be
                          met as part of the definition of the extension.
                        type: array
                        title: Additional content defined by implementations
                        items:
                          type: Extension
                        element_property: 'true'
                      modifierExtension:
                        element_property: 'true'
                        description: '''May be used to represent additional information that
                          is not part of the basic definition of the resource and that modifies
                          the understanding of the element that contains it and/or the understanding
                          of the containing element''''s descendants. Usually modifier elements
                          provide negation or qualification. To make the use of extensions safe
                          and manageable, there is a strict set of governance applied to the
                          definition and use of extensions. Though any implementer is allowed
                          to define an extension, there is a set of requirements that SHALL
                          be met as part of the definition of the extension. Applications processing
                          a resource are required to check for modifier extensions.  Modifier
                          extensions SHALL NOT change the meaning of any elements on Resource
                          or DomainResource (including cannot change the meaning of modifierExtension
                          itself).'''
                        items:
                          type: Extension
                        title: Extensions that cannot be ignored
                        type: array
                      resource_type:
                        const: OperationOutcome
                        type: string
                        default: OperationOutcome
                        title: Resource Type
                      contained:
                        title: Contained, inline Resources
                        element_property: 'true'
                        type: array
                        description: These resources do not have an independent existence apart
                          from the resource that contains them - they cannot be identified independently,
                          and nor can they have their own independent transaction scope.
                        items:
                          type: Resource
                      _implicitRules:
                        title: Extension field for ``implicitRules``.
                        type: FHIRPrimitiveExtension
                      implicitRules:
                        type: string
                        element_property: 'true'
                        title: A set of rules under which this content was created
                        pattern: S*
                        description: A reference to a set of rules that were followed when the
                          resource was constructed, and which must be understood when processing
                          the content. Often, this is a reference to an implementation guide
                          that defines the special rules along with other profiles etc.
                      text:
                        type: Narrative
                        element_property: 'true'
                        title: Text summary of the resource, for human interpretation
                        description: A human-readable narrative that contains a summary of the
                          resource and can be used to represent the content of the resource
                          to a human. The narrative need not encode all the structured data,
                          but is required to contain sufficient detail to make it "clinically
                          safe" for a human to just read the narrative. Resource definitions
                          may define what content should be represented in the narrative to
                          ensure clinical safety.
                      language:
                        description: The base language in which the resource is written.
                        title: Language of the resource content
                        pattern: ^[^s]+(s[^s]+)*$
                        type: string
                        element_property: 'true'
                      issue:
                        type: array
                        element_property: 'true'
                        title: A single issue associated with the action
                        items:
                          type: OperationOutcomeIssue
                        description: An error, warning, or information message that results
                          from a system action.
                    description: '''Disclaimer: Any field name ends with ``__ext`` doesn''''t
                      part of Resource StructureDefinition, instead used to enable Extensibility
                      feature for FHIR Primitive Data Types.  Information about the success/failure
                      of an action. A collection of error, warning, or information messages
                      that result from a system action.'''
                    example:
                      issue:
                        '0':
                          details:
                            text: Bad Request
                          severity: error
                          code: invalid
                      id: '101'
                      resourceType: OperationOutcome
                    required:
                      '0': issue
                    title: OperationOutcome 400
                    additionalProperties: 'false'
                    type: object
                description: Patient create request could not be parsed or failed basic FHIR
                  validation rules.
              '201':
                description: Successful Patient create
                content:
                  application/fhir+json:
                    schema:
                      ref: '#/components/schemas/Patient'
                      description: The Patient create interaction creates a new Patient resource in a
                        server-assigned location.
                      operationId: fhirstarter|type|create|post|Patient
                      tags:
                        '0': Type:Patient
                      parameters:
                        '0':
                          schema:
                            type: string
                            title: Format
                            description: Override the HTTP content negotiation to specify JSON or XML
                              response format
                          in: query
                          required: 'false'
                          description: Override the HTTP content negotiation to specify JSON or XML response
                            format
                          name: _format
                        '1':
                          schema:
                            type: string
                            description: Ask for a pretty printed response for human convenience
                            title: Pretty
                          name: _pretty
                          required: 'false'
                          in: query
                          description: Ask for a pretty printed response for human convenience
                      requestBody:
                        content:
                          application/fhir+json:
                            schema:
                              ref: '#/components/schemas/Patient'
---

