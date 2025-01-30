pageextension 72700 ItemDetails extends "Item Card"
{
    layout
    {
        addlast(content)
        {
            field("Last DateTime Modified"; Rec."SystemModifiedAt")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
            field("Global Dimension 1 Code"; Rec."Global Dimension 1 Code")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
            field("Global Dimension 2 Code"; Rec."Global Dimension 2 Code")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
            field("Substitutes Exist"; Rec."Substitutes Exist")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
        }
    }
}

pageextension 72701 CustomerDetails extends "Customer Card"
{
    layout
    {
        addlast(content)
        {
            field("Last DateTime Modified"; Rec."SystemModifiedAt")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
        }
    }
}

pageextension 72702 ContactDetails extends "Contact Card"
{
    layout
    {
        addlast(content)
        {
            field("Last DateTime Modified"; Rec."SystemModifiedAt")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
            field("First Name"; Rec."First Name")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
            field("Surname"; Rec."Surname")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
        }
    }
}

page 72703 ItemAttributeValueMapping
{
    SourceTable = "Item Attribute Value Mapping";

    layout
    {
        area(content)
        {
            field("Last DateTime Modified"; Rec."SystemModifiedAt")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
            field(No; Rec."No.")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
            field("Item Attribute ID"; Rec."Item Attribute ID")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
            field("Item Attribute Value ID"; Rec."Item Attribute Value ID")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
        }
    }
}

page 72704 ItemAttribute
{
    SourceTable = "Item Attribute";

    layout
    {
        area(content)
        {
            field("Last DateTime Modified"; Rec."SystemModifiedAt")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
            field("ID"; Rec."ID")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
            field("Name"; Rec."Name")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
        }
    }
}

page 72705 ItemAttributeValue
{
    SourceTable = "Item Attribute Value";

    layout
    {
        area(content)
        {
            field("Last DateTime Modified"; Rec."SystemModifiedAt")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
            field("ID"; Rec."ID")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
            field("Attribute ID"; Rec."Attribute ID")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
            field("Value"; Rec."Value")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
        }
    }
}

pageextension 72706 MachineCenterDetails extends "Machine Center Card"
{
    layout
    {
        addlast(content)
        {
            field("Last DateTime Modified"; Rec."SystemModifiedAt")
            {
                ApplicationArea = Basic, Suite;
                Visible = false;
            }
        }
    }
}