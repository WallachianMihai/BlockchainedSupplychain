package com.example.manufacturergui.model;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
public class Inventory
{
    Integer id;
    String productName;
    Integer quantity;

    public Inventory(Integer id, String productName, Integer quantity)
    {
        this.id = id;
        this.productName = productName;
        this.quantity = quantity;
    }
}
