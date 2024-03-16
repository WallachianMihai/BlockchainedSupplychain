package com.example.manufacturergui.model;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class Customer
{
    private Integer id;
    private String name;
    private String location;

    public Customer(Integer id, String companyName, String location)
    {
        this.id = id;
        this.name = companyName;
        this.location = location;
    }

}
